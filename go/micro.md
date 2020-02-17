# go-micro

## 1 安装

- 安装golang version>=1.13
- micro-gen: go get github.com/micro/protoc-gen-micro/v2
  
``` bash
protoc --proto_path=. --micro_out=. --go_out=. proto/greeter.proto
```
- import: "github.com/micro/go-micro/v2"
- go get github.com/micro/micro@v1.18    //v2编译失败
- demo
  
``` go
package main

import (
	"context"
	"fmt"
	proto "micro_test/proto"

	"github.com/micro/go-micro/v2"
)

type Greeter struct{}

func (g *Greeter) Hello(ctx context.Context, req *proto.Request, rsp *proto.Response) error {
	rsp.Greeting = "Hello " + req.Name
	return nil
}

func main() {


	// Create a new service. Optionally include some options here.
	service := micro.NewService(
		micro.Name("greeter"),
	)

	// Init will parse the command line flags.
	service.Init()

	// Register handler
	proto.RegisterGreeterHandler(service.Server(), new(Greeter))

	// Run the server
	if err := service.Run(); err != nil {
		fmt.Println(err)
	}
}


```

## 2.概念

- micro 与 go-micro
  - micro是一套工具库，提供指令：
    - api  	API 网关，独立HTTP入口，由服务发现实现动态路由
    - web	Web DashBoard	UI，管理监控界面
    - cli	命令行接口
    - bot	Slack与Hipchat bot ?
    - new	服务构建模板
    - call  发起客户端请求
    - broker 启动消息转发
    - proxy	 启动服务代理
  - go micro 微服务开发框架


#### 参考
- [简书](https://www.jianshu.com/p/751cd31302e7)