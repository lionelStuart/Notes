### 有序队列合并

#### 题目
有道面试题出的挺不错，做的时候没有答好，事后总结一下。

golang实现任意数量的有序数组合并，函数原型如下：
```
func Sort(ctx context.Context, out chan<- int, in ... <-chan int)
```
有序数列通过任意数量的chan输入，所以可能随时增加，输出通过out chan得到

#### 分析
leetcode上有类似的题目，思路比较简单。这个题的难点在如何访问chan的元素，一旦取出就不好放回。

当时先考虑使用切片作为buf，从chan中遍历的数先放到切片，再遍历切片找最小的数。切片的问题是不好判断一个数是取出还是放回的状态。下次再遍历chan时也不好判断哪个切片存了放回的值。

接着就会想到用chan作为buf,使用长度为1的buf，满的话说明还有值，空的话就补充值。

所以思路是这样的：创建一组长度均为1的chan作为buf，每轮循环先从out chan取值存到buf chan,然后遍历buf chan，找到最小值，每次比较后，把较大的值放回buf chan 原来的位置。

#### 代码实现

定义buf结构如下，Tmp为长度1的chan,取出的元素放到Curr做比较
``` go
type Head struct {
	Curr int
	Tmp chan int
}
```

还有一些细节需要处理;
- 这里需要使用ctx.Done()处理函数退出
- 从in读入值时，需要判断是否读取成功
- 从in读入值时，需要非阻塞的读取
- 如果管道全部读完，可以考虑计数为0后退出，或者传入的ctx超时，有没有更好的办法？
- 每轮比较只从buf中读出1个值，其他元素需要放回，所以要记录当前最小值的位置
- 在遍历Head存取元素前，都要先判断Tmp的长度

得到代码实现如下
``` go
func Sort(ctx context.Context, out chan<- int, in ... <-chan int) {
	//初始化buf
	var heads [] Head
	for i:=0;i!=len(in);i++{
		heads = append(heads, Head{
			Tmp:make(chan int,1),
		})
	}
    ticker := time.NewTicker(time.Millisecond*10)
    
	for{
		select {
			case <-ctx.Done():
				// 处理退出
				ticker.Stop()
				return
			case <-ticker.C:
				count := 0
				for i,head := range heads{
					//还有值，不读入
					if len(head.Tmp) == 1{
						count++
						continue
					}
					//非阻塞读入
					select {
					case v,ok :=<-in[i]:
						// 判断是否可读
						if ok{
							head.Tmp<-v
							count ++
						}
					default:
					}
				}
				if count == 0{
					return
				}
				
				// 标记最小值的通道号和值
				minId :=-1
				var min int

				for i,head := range heads{
					// 为空的跳过
					if len(head.Tmp) == 0{
						continue
					}
					
					head.Curr=<-head.Tmp
					// 初始化最小值
					if minId == -1{
						minId = i
						min = head.Curr
						continue
					}
					// 比较最小值
					if minId !=-1{
						if head.Curr<min{
							//放回旧的值
							heads[minId].Tmp<-min
							minId = i
							min = head.Curr
						} else{
							//放回新的值
							head.Tmp<-head.Curr
						}
					}
				}
				//输出最小值
				if minId!=-1{
					out<-min
				}
		}
	}
}
```

测试样例如下
``` go
func main() {
	ctx, cancel := context.WithCancel(context.Background())
	out := make(chan int,100)
	in1 := make(chan int,10)
	in2 := make(chan int,10)
	for i:=0;i!=10;i++{
		in1<-i+1

	}
	for i:=0;i!=10;i++{
		in2<-i+3
	}

	go Sort(ctx, out, in1, in2)
	time.Sleep(time.Second*3)

	cancel()
	close(out)
	time.Sleep(time.Second*1)
	fmt.Println("end==")
	for i := range out{
		fmt.Print(i)
	}
}
```