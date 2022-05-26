##  golang并发

###  1. worker Pool

启动一个工作池，启动maxRoutines个routine，轮询works，满时阻塞任务添加

#### 1.1 接口
``` go
type Worker interface{
    Task()
}
// 实现自定义Worker

type WorkPool interface {
    Run(w Worker)
    Shutdown()
}
// Run 向Worker添加任务
// Shutdown 终止任务

type WorkerConstruction func(maxRoutines int) *WorkPool
// 构造WorkPool

type WorkPool struct {
	works chan Worker
	wg sync.WaitGroup
}
// works 向Worker添加任务
// wg 控制任务调度
```

#### 1.2 实现

``` go
func NewWorkPool(maxRoutines int) *WorkPool{
	wp := &WorkPool{
		works:make(chan Worker),
	}
	wp.wg.Add(maxRoutines)
	for i:=0;i!=maxRoutines;i++{
        // 启动N个routine, 每一个都range works，chan会确保这没有冲突
		go func(){
			for w := range wp.works{
				w.Task()
			}
			wp.wg.Done()
		}()
	}

	return wp
}

func (p *WorkPool) Run(w Worker){
	p.works<-w
	// 通过管道添加任务
}

func(p *WorkPool) Shutdown(){
	close(p.works)
	// 关闭chan, 停止写入,wait 等待任务完成
	// 在close的chan上执行range不会阻塞
	p.wg.Wait()
}
```

####  1.3 测试
``` go
// 测试任务 
type DemoWork struct {
	workmate string
}

// 模拟任务，睡两秒
func (d *DemoWork) Task() {
	time.Sleep(time.Second*2)
	fmt.Printf("work:  %s \n", d.workmate)
}

func TestWorkPool_Run(t *testing.T) {
	// 最多并发四个任务
	p := NewWorkPool(4)
	// 在任务结束前阻塞在Shutdown
	defer p.Shutdown()
    
    //每四个一组有序，任务总耗时预计在6秒
	for i:=0;i!=10;i++{
		p.Run(&DemoWork{workmate: fmt.Sprintf("sample-%d", i)})
	}
}
```

###  2. runner
构造一个runner 队列，按顺序依次执行队列任务，遇到中断和超时时终止

#### 2.1 接口
``` go
type WorkFunc (int) 
// 任务

type RunnerConstruction func() *Runner
// 构造runner

type Runner interface {
    Start(d time.Duration) error
    Add(task ... WorkFunc) error
}
// start 启动一个带超时的Runner
// Add 增加任务

```

####  2.2 实现
``` go
type Runner struct {
	interrupt chan os.Signal
	complete chan error
	timeout <-chan time.Time
	tasks []func(id int)
}
// interrupt 接收中断
// timeout 接收超时
// complete 阻塞完成，输出错误
// tasks 添加任务队列

var (
	ErrTimeout   = errors.New("recv timeout")
	ErrInterrupt = errors.New("recv interrupt")
)

func NewRunner() *Runner {
	return &Runner{
		interrupt: make(chan os.Signal),
		complete:  make(chan error),
		timeout:   make(chan time.Time),
	}
}

func (r *Runner) Start(d time.Duration) error {
	signal.Notify(r.interrupt, os.Interrupt)
    // 通知注册信号
	ctx, _ := context.WithTimeout(context.Background(), d)
    // 启动带超时的routine
	go func() {
		r.complete <- r.run(ctx)
	}()
    
    // 阻塞在complete
	return <-r.complete
}

func (r *Runner) Add(task ...func(int)) {
	r.tasks = append(r.tasks, task...)
}
// 添加任务队列

func (r *Runner) run(ctx context.Context) error {
	for id, task := range r.tasks {
		select {
		// 返回超时
		case <-ctx.Done():
			return ErrTimeout
		// 返回中断
		case sig := <-r.interrupt:
			fmt.Printf("recv interrupt %+v", sig)
			return ErrInterrupt
		// 执行任务
		default:
			task(id)
		}

	}

	return nil
}
```

####  2.3 测试

``` go
func TestRunner_Timeout(t *testing.T) {
	r := NewRunner()

    // 模拟任务，睡1秒
	worker := func(id int){
		time.Sleep(time.Second*1)
		fmt.Println("== end worker ", id)
	}
    
    // 增加8个任务，定时5秒，仅能执行完5个任务
	for i := 0;i!=8;i++{
		r.Add(worker)
	}

	err :=r.Start(time.Second*5)
	if err !=nil{
		t.Log(err)
	}
}
```

###  3. 资源池
资源池提供可重复使用的资源, 资源需实现io.closer 

####  3.1 接口

``` go 
// 资源构造函数, 资源需实现io.Closer 接口
type Factory = func() (io.Closer, error)

type Pool interface {
    Acquire()(io.Closer, error)
    Release(r io.Closer)
    Close()
}
// 获取，释放，关闭

type PoolConstruction func() *Pool
// 构造Pool
```

####  3.2 实现
```
type Pool struct {
	m sync.Mutex

	resources chan io.Closer
	factory   Factory
	closed    bool
}
// 资源释放和close需要互斥锁
//resources 存放对象
// factory 存放资源构造方法

var (
	InvalidSizeErr = errors.New("invalid pool size")
	PoolCloseErr   = errors.New("pool may closed")
)

const (
	PI float32 = 3.1415926
)

func NewPool(fn Factory, size uint) (*Pool, error) {
	if size <= 0 {
		return nil, InvalidSizeErr
	}

	return &Pool{
		factory:   fn,
		resources: make(chan io.Closer, size),
		closed:    false,
	}, nil
	// 创建开始池中没有资源，release后拥有可复用的资源
}

func (p *Pool) Acquire() (io.Closer, error) {
	select {
	case r, ok := <-p.resources:
	    // 若关闭, ok为false
		if !ok {
			return nil, PoolCloseErr
		}
		return r, nil
	default:
	    // resources为空阻塞，执行默认
		return p.factory()
	}
}
// 有资源可获取则返回，否则使用factory 方法进行构造

func (p *Pool) Release(r io.Closer) {
	p.m.Lock()
	defer p.m.Unlock()

	if p.closed {
		r.Close()
		return
	}

	select {
	case p.resources <- r:
	    //未满，非阻塞，可放回
		fmt.Println("release resources success")
	default:
	    // 已满，阻塞，执行默认
		fmt.Println("fail release")
		r.Close()
	}
}
// 放回资源前需要先判断pool是否关闭
// 无论是否放回成功都需要close资源

func (p *Pool) Close() {
	p.m.Lock()
	defer p.m.Unlock()

	if p.closed{
		return
	}
	p.closed = true
	close(p.resources)

	for i := range p.resources {
		i.Close()
	}

}
// 如果已经关闭pool则不需要再次关闭
// 关闭pool 先关闭resource写入，再执行资源的close
```

####  3.3 测试
``` go
type SampleConnection struct {
	ID int32
}

func (sc SampleConnection) Close() error {
	fmt.Println("close current conn :", sc.ID)
	return nil
}

func (sc SampleConnection) Ping() string {
	return fmt.Sprintf("pong from : %d ", sc.ID)
}

var idCount int32

func init() {
	idCount = 0
}

func NewSampleConnection() (io.Closer, error) {
	id := atomic.AddInt32(&idCount, 1)
	return & SampleConnection{
		ID: id,
	}, nil
}
// 构造SampleConnection 对象

//测试资源的获取和释放
func TestPool_Release(t *testing.T) {
	p, _ := NewPool(NewSampleConnection, 2)
	defer p.Close()
	var acquiredRes [] *SampleConnection

	for i := 0; i != 3; i++ {
		res, err := p.Acquire()
		if err != nil {
			t.Error(err)
		}
		//类型转换需要一致
		if conn, ok:= res.(*SampleConnection); ok {
			t.Log("recv ", conn.Ping())
			acquiredRes = append(acquiredRes, conn)
		} else {
			t.Logf("err %t %#+v \n", ok, res)
		}

		t.Logf("res: %+v \n", res)

	}

	for _,v:= range acquiredRes{
		p.Release(v)
	}
}

```

### 4. Map-Reduce 
对输入列表的资源，先按map分routine执行，归并结果，执行reduce

####  4.1 接口
```  go
type MapReduceWork interface {
	Map(list list.List) interface{}
	Reduce(list list.List) interface{}
}
// 定义MapReduce 任务接口

type MapReduceExecutor interface{
    Start()
    Add(work MapReduceWork, resources list.List)
}
// Start 启动任务, Add增加任务原型和资源

type NewMRExecuter func(maxRoutine int) *MapReduceExecutor
// 构造mp执行器
```

####  4.2 实现

```  go
type MapReduceExecutor struct {
	MaxRoutine int
	wg         sync.WaitGroup
	mid        chan interface{}

	work MapReduceWork
	resource list.List
}
// maxRoutine 确定map 阶段最大routine 数
// wg 控制map 执行
// mid 存放map阶段结果
// work为工作原型
// 资源为输入资源

func NewMRExecuter(maxRoutine int) *MapReduceExecutor {
	return &MapReduceExecutor{
		MaxRoutine: maxRoutine,
		mid:        make(chan interface{}, maxRoutine),
	}
}

func (e *MapReduceExecutor) Start() {
	e.wg.Add(e.MaxRoutine)
    
    // 将资源按routine数目拆分为N片
	split := make([]list.List,e.MaxRoutine)
	count :=0
	for i:=e.resource.Front();i!=nil;i=i.Next(){
		count +=1
		split[count%e.MaxRoutine].PushBack(i.Value)
	}
	// 执行map任务
	for i := 0;i<e.MaxRoutine;i++{
		go func(i int) {
			e.mid <- e.work.Map(split[i])
			e.wg.Done()
		}(i)
	}
    
    // 等待任务执行结束
	e.wg.Wait()
	close(e.mid)
	// 合并map 任务
	var reduces  list.List
	for p := range e.mid{
		reduces.PushBack(p)
	}
	// 执行reduce 任务
	result := e.work.Reduce(reduces)
	fmt.Printf("result %+v \n", result)
}

func (e *MapReduceExecutor) Add(work MapReduceWork, resource list.List) {
	e.work = work
	e.resource = resource
}
//增加执行任务和资源

```

####  4.3 测试

```  go

// 模拟map-reduce 任务
type SampleWork struct {

}

//map 累加和
func (s SampleWork) Map(list list.List) interface{}{
	total :=0
	for i := list.Front();i!=nil;i = i.Next(){
		if v,ok := i.Value.(int); ok{
			total += v
		}

	}
	fmt.Println("sam map result ",total)
	return total
}

// reduce 累加和
func (s SampleWork) Reduce(list list.List) interface{}{
	total :=0
	for i := list.Front();i!=nil;i = i.Next(){

		if v,ok := i.Value.(int); ok{
			total += v
		}

	}
	return total
}

// 测试map-reduce任务
func TestMapReduceExecutor_Start(t *testing.T) {
    // map阶段启用4个routine
	mpExec := NewMRExecuter(4)

	in := list.List{}
	for i:= 0;i!=1000;i++{
		in.PushBack(i)
	}

	mpExec.Add(SampleWork{}, in)
	mpExec.Start()

}
```

### 参考
- 《go语言实战》