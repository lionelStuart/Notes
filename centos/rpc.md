# rpc

## 1. rpc & rest

### 1.1 rest

- REST， 通过HTTP协议定义动词（GET POST PUT DELETE）,对网络资源进行唯一标识，无状态通信
- HTTP协议和URL用于统一接口和定位资源，文本，二进制，xml,json用于表述资源
  

### 1.2 rpc

- 像调用本地服务一样调用服务器上的服务，按响应方式分为同步调用和异步调用(将消息发送给中间件后返回，继续操作)
- rpc框架
  - client 调用方
  - client stub 调用方存根，序列/反序列化，收发请求
  - server stub 提供方存根，序列/反序列化，收发请求
  - server 提供方
- 目的： 封装调用，序列/反序列化过程 Serialize Marshal

### 1.3 rest & rpc 选型

- 调用方式：rest需要关注网络传输，rpc客户端通过接口直接发起，只关注业务调用，开发更高效； 性能角度：http状态描述，扩展更丰富，但携带信息多，性能更低效；运维：http需要前端代理，扩容时，需修改代理服务器配置，rpc仅增加服务节点，通过注册中心感知节点变化，更高效
- 组织边界：边界内使用rpc;边界外使用rest


## 2. go rpc

## 3. protobuf
### 3.1 概念
- 优势
  - 简单，相比于xml
  - 效率，体积，速度，二进制编码
  - 生成数据访问类
  - 自动的序列化/反序列化
  - 可以作为自描述格式，用于存储
  - 作为协议文件的一部分
  - 兼容性好，使用tag标记字段，协议新增字段，对于旧的服务，可以跳过不解析
-  proto3 语法
     - message 类型命名驼峰体，字段命名下划线
     - enum 类型命名驼峰体，字段命名大写下划线
     - 类型
       - double float bool
       - int32 int64 uint32 uint64 
       - sint32 sint64             for negative
       - fix32 fix64               for large number 2^32 2^56
       - sfix32 sfix64             4/8 bytes
       - string
       - bytes
     - repeated 数组
     - singular 可选
     - 嵌套类型
     - package foo.bar; 包名，防止重名
     - 增加对json的支持
- 编码方式，类似于TLV，tag = field_number + wire_type (varints)
  - 0 varint [int31,int64,uint32,bool.enum..] TV
  - 1/5 64-bit[fix64,double] /32-bit[fix32,float] TV
  - 2 Length-delimited [string, bytes,packed repeated, embedded messages] TLV
  - 编码策略：variant, zigzag
    - variant利用1bit作为msb,因此可以去掉length, 对非符号，小的正数效率高，编码负数效率降低(int32,int64);
    - zigzag,有符号整数映射无符号整数后使用variant(sint32,sint64)
    - tag, 占用1-15，超出时新增一个字节

- demo

``` bash
// generate 
protoc --go_out=plugins=grpc:. xxx.proto
```

``` pb

syntax = "proto3";

message SongRequest {
  string song_name = 1;
}

message SongResponse {
  string song_name = 1;
}

enum Foo {
  FIRST_VAL = 0;
  SECOND_VAL = 1;

}

service SongService {
  rpc GetSong(SongRequest) returns (SongResponse)
}

// 双向流
service DoubleService {
  rpc Channel(stream String) returns (stream String);
}

// 单向流
service SingleService {
  rpc ListFeatures() returns (stream Features);
  rpc Record(stream Point) return (string);
}



```

## 4. grpc

### 4.1 安装
- protoc 配置到$GOROOT/bin
- go get -u google.golang.org/grpc
- go get -u github.com/golang/protobuf/protoc-gen-go
- --go_out 指定plugins及输出目录， --proto_path指定proto文件位置
  
``` bash
protoc --go_out=plugins=grpc:proto --proto_path=proto hello.proto pubsub.proto
```
### 4.2 demo
- 客户端 / 服务端实现

hello.pb
``` pb
syntax = "proto3";

package Hello;

message String {
    string value =1;
}

service HelloService {
    rpc Hello (String) returns (String);
}
```

test.go
``` go
type HelloSvcImpl struct {
}

func (p *HelloSvcImpl) Hello(ctx context.Context, args *Hello.String) (*Hello.String, error) {
	reply := &Hello.String{Value: "hello: " + args.GetValue()}
	return reply, nil
}

func TestGRpc(t *testing.T) {
	go func() {
		server := grpc.NewServer()
		Hello.RegisterHelloServiceServer(server, &HelloSvcImpl{})
		lis, err := net.Listen("tcp", ":2234")
		if err != nil {
			t.Fatal("fail ", err)
		}
		server.Serve(lis)

	}()

	time.Sleep(time.Second * 3)

	conn, err := grpc.Dial(":2234", grpc.WithInsecure())
	if err != nil {
		t.Fatal("cli fail", err)
	}
	defer conn.Close()

	cli := Hello.NewHelloServiceClient(conn)
	rep, err := cli.Hello(context.Background(), &Hello.String{Value: "grpc world"})
	if err != nil {
		t.Fatal("cli fail", err)
	}
	t.Log(rep.GetValue())
}

```

### 4.3 grpc流

``` pb
service HelloService {
    rpc Hello (String) returns (String);
    rpc Channel (stream String) returns (stream String);
}
```

``` go
// 服务实现
func (p *HelloSvcImpl) Channel(stream Hello.HelloService_ChannelServer) error {
	for{
		args, err := stream.Recv()
		if err !=nil{
			if err == io.EOF{
				return nil
			}
			return err
		}

		reply := &Hello.String{Value:"hello: " + args.GetValue()}
		err = stream.Send(reply)
		if err !=nil{
			return err
		}
	}
}


func TestGpcStream(t *testing.T){
// server
	go func() {
		server := grpc.NewServer()
		Hello.RegisterHelloServiceServer(server, &HelloSvcImpl{})
		lis, err := net.Listen("tcp", ":2234")
		if err != nil {
			t.Fatal("fail ", err)
		}
		server.Serve(lis)

	}()
	
	time.Sleep(time.Second * 3)

// client
	conn, err := grpc.Dial(":2234", grpc.WithInsecure())
	if err != nil {
		t.Fatal("cli fail", err)
	}
	defer conn.Close()


	cli := Hello.NewHelloServiceClient(conn)
	stream, err := cli.Channel(context.Background())
	if err != nil {
		t.Fatal("cli fail", err)
	}

//send
	go func() {
		for count:=0;;count++{
			if err :=stream.Send(&Hello.String{
				Value:fmt.Sprintf("count %d",count)});err !=nil{
				t.Fatal("fail send",err)
			}
			time.Sleep(time.Second)
		}
	}()

//recv
	ch :=make(chan Hello.String,2)
	go func(ch chan <- Hello.String){
		for{
			reply,err := stream.Recv()
			if err !=nil{
				if err == io.EOF {
					ch <-Hello.String{Value:"Done"}
					break
				}
				t.Fatal("fail recv",err)
			}
			ch <- *reply
		}
	}(ch)

	for count:=0;count !=10;count++{
		msg :=<-ch
		t.Log("recv: ",msg.GetValue())
	}
}

```

### 4.4 发布/订阅服务

使用docker项目提供的pubsub包实现本地发布订阅

```
import "hello.proto";

service PubSubService{
    rpc Publish (String) returns (String);
    rpc Subscribe (String) returns (stream String);
}
```

pubsub.go 发布订阅的服务实现
- 服务实现
``` go 
type PubSubSvc struct {
	pub *pubsub.Publisher
}

func NewPubSubService() *PubSubSvc{
	return &PubSubSvc{
		pub:pubsub.NewPublisher(100*time.Millisecond,10),
	}
}

func (p *PubSubSvc) Publish(ctx context.Context,
	args *Hello.String)(*Hello.String, error){
	p.pub.Publish(args.GetValue())
	return &Hello.String{},nil
}

func (p *PubSubSvc) Subscribe(args *Hello.String, stream Hello.PubSubService_SubscribeServer) error{
  // 注册一个过滤器函数，过滤 topic
	ch := p.pub.SubscribeTopic(func(v interface{}) bool{
		if k, ok := v.(string);ok{
			if strings.HasPrefix(k, args.GetValue()){
				return true
			}
		}
		return false
	})

	for v:=range ch{
		if err :=stream.Send(&Hello.String{Value:v.(string)});err !=nil{
			return err
		}
	}
	return nil

}
```
- 测试demo
``` go
func TestPubSub(t *testing.T){
	//server
	go func() {
		server := grpc.NewServer()
		svc := NewPubSubService()
		Hello.RegisterPubSubServiceServer(server, svc)
		lis, err := net.Listen("tcp", ":2234")
		if err != nil {
			t.Fatal("fail ", err)
		}
		server.Serve(lis)

	}()

	time.Sleep(time.Second)
	//publisher
	go func(){
		conn,err := grpc.Dial(":2234",grpc.WithInsecure())
		if err !=nil{
			t.Fatal(err)
		}
		defer conn.Close()

		cli := Hello.NewPubSubServiceClient(conn)
		for i :=0;i!=3;i++{
			_,err := cli.Publish(
				context.Background(), &Hello.String{Value:fmt.Sprintf("golang %d",i)})
			if err !=nil{
				t.Fatal(err)
			}

			_,err = cli.Publish(
				context.Background(), &Hello.String{Value:fmt.Sprintf("docker %d",i)})
			if err !=nil{
				t.Fatal(err)
			}
		}
	}()

	// subscriber
	go func() {
		conn, err := grpc.Dial(":2234",grpc.WithInsecure())
		if err !=nil{
			t.Fatal(err)
		}
		defer conn.Close()

    cli := Hello.NewPubSubServiceClient(conn)
    // 只订阅主题为golang
		stream,err := cli.Subscribe(context.Background(), &Hello.String{Value:"golang"})
		if err !=nil{
			t.Fatal(err)
		}
		for {
			reply, err := stream.Recv()
			if err !=nil{
				if err == io.EOF{
					break
				}
				t.Fatal(err)
			}
			t.Log(reply.GetValue())
		}
	}()

	time.Sleep(time.Second*15)
}
```

### 4.5 grpc 网关
  - 安装
``` bash
go install \
    github.com/grpc-ecosystem/grpc-gateway/protoc-gen-grpc-gateway \
    github.com/grpc-ecosystem/grpc-gateway/protoc-gen-swagger \
    github.com/golang/protobuf/protoc-gen-go
```
  - 定义proto文件

rest.proto
``` pb
syntax="proto3";

package Hello;

import "google/api/annotations.proto";

message StringMessage {
    string value =1;
}

service RestService{
    rpc Get(StringMessage) returns (StringMessage){
        option (google.api.http) = {
        get:"/get/{value}"
        };
    }
    rpc Post(StringMessage) returns (StringMessage) {
        option (google.api.http) = {
        post:"/post"
        body:"*"
        };
    }
}
```

 - 生成pb.go 和 pb.gw.go

由于上述插件使用了go mod 进行安装，尝试按照官方给的指令-I导入src 或 pkg/mod 下的import路径均失败，解决的办法是将protobuf和grp-gateway/third-party/googleapis下的proto文件夹全部拷贝到本地


```
// 生成grpc 文件
protoc    --proto_path=proto --go_out=plugins=grpc:proto  rest.proto

// 生成grpc和groc-gw文件
protoc    --proto_path=proto --go_out=plugins=grpc:proto  --grpc-gateway_out=proto  rest.proto
```

- 编译服务代码

服务编译错误：grpc.SupportPackageIsVersion，
尝试更新包版本 
```
go get -u github.com/golang/protobuf/{proto,protoc-gen-go}
go get -u google.golang.org/grpc
gomod中replace的版本更新到1.17
```

- 服务实现

``` go
package main

import (
	"context"
	"google.golang.org/grpc"
	"net"
	Rest "sisyphus/common/rpc/proto"
)

type RestSvcImpl struct {

}

func (r *RestSvcImpl) Get(ctx context.Context, message *Rest.StringMessage) (*Rest.StringMessage,error){
	rep := &Rest.StringMessage{Value:"rest: "+ message.GetValue()}
	return rep, nil
}

func (r *RestSvcImpl) Post(ctx context.Context, message *Rest.StringMessage) (*Rest.StringMessage,error){
	rep := &Rest.StringMessage{Value:"rest post: "+ message.GetValue()}
	return rep, nil
}

func main() {
	server := grpc.NewServer()
	Rest.RegisterRestServiceServer(server, &RestSvcImpl{})
	lis, err := net.Listen("tcp", ":2234")
	if err != nil {
		panic( err)
	}
	server.Serve(lis)
}

```

- 网关实现

``` go
package main

import (
	"context"  // Use "golang.org/x/net/context" for Golang version <= 1.6
	"flag"
	"net/http"

	"github.com/golang/glog"
	"github.com/grpc-ecosystem/grpc-gateway/runtime"
	"google.golang.org/grpc"

	gw "sisyphus/common/rpc/proto"  // Update
)

var (
	// command-line options:
	// gRPC server endpoint 反向代理指定的端口
	grpcServerEndpoint = flag.String("grpc-server-endpoint",  "localhost:2234", "gRPC server endpoint")
)

func run() error {
	ctx := context.Background()
	ctx, cancel := context.WithCancel(ctx)
	defer cancel()

	// Register gRPC server endpoint
	// Note: Make sure the gRPC server is running properly and accessible
	mux := runtime.NewServeMux()

	opts := []grpc.DialOption{grpc.WithInsecure()}
	err := gw.RegisterRestServiceHandlerFromEndpoint(ctx, mux,  *grpcServerEndpoint, opts)
	if err != nil {
		return err
	}

	// Start HTTP server (and proxy calls to gRPC server endpoint)
	// 在8081端口监听请求
	return http.ListenAndServe(":8081", mux)
}

func main() {
	flag.Parse()
	defer glog.Flush()

	if err := run(); err != nil {
		glog.Fatal(err)
	}
}

```

- 测试指令
```
curl localhost:8081/get/gorpc

curl -XPOST localhost:8081/post --data '{"value":"grpc"}'
```




#### 参考
- Go语言高级编程
- [csdn 博客](https://blog.csdn.net/u014590757/article/details/80233901)