
## 1. 信号

### 1.1 常用信号


|  信号   |  值   | 动作  |         说明         |
| :-----: | :---: | :---: | :------------------: |
|  SIGUP  |   1   | Term  |     终端连接中断     |
| SIGINT  |   2   | Term  | 用户发送INTR:ctrl+c  |
| SIGQUIT |   3   | Core  | 用户发送QUIT:ctrl+/  |
| SIGKILL |   9   | Term  | 无条件结束，无法捕获 |
| SIGTERM |  15   | Term  |    结束，可被捕获    |

### 1.2 go实现

- 创建管道，连接os.Signal
- os.Signal Notify 指定信号
- while ：=<-c 循环捕获
- switch/case 处理信号

``` go
	c := make(chan os.Signal, 1)
	signal.Notify(c, syscall.SIGHUP, syscall.SIGQUIT, syscall.SIGTERM, syscall.SIGINT)

	for {
		s := <-c
		fmt.Println("recv sig")
		switch s {
		case syscall.SIGQUIT, syscall.SIGTERM, syscall.SIGINT:
			fmt.Println("quit ...")
			return
		case syscall.SIGHUP:
			fmt.Println("sighup ...")
		default:
			fmt.Println("default ...")
			return
		}
	}
```

## 2. 测试

### 2.1 测试框架

- 创建测试
1. 创建后缀名为XX_test.go 的文件
2. 创建函数 TestXXX(test *testing.T){}
3. 记录测试信息
    
    log记录信息，Fatalf用于记录严重错误，FailNow标记错误信息并立刻退出，
``` go
func TestRunSampleA(t *testing.T) {
	t.Log("test a")
	for i := 0; i != 10; i++ {
		if i > 6 && i <= 8 {
			// 记录错误信息
			t.Errorf("err output %d", i)
			//标记当前错误
			t.Fail()
		} else if i > 8 {
			// 记录严重信息
			t.Fatalf("curical output %d", i)
			//标记错误并退出
			t.FailNow()
		} else {
			//记录信息
			t.Logf("curr output %d", i)
		}
	}
	t.Log("expect success return ..")
}
```
4. 其他测试

    Skip 跳过当前测试 Parallel开启并行测试，Example启用一条样例测试
``` go
func ExampleTestA(){
	fmt.Println("hello")
	//Output:hello a
}
```

## 3.web基础

### 3.1 hello world
``` go
func main() {
	http.HandleFunc("/",sayHello)						//设置路由
	err := http.ListenAndServe(":9090",nil)		//设置监听
	if err!=nil{
		log.Fatal("listen and serve ",err)
	}

}

func sayHello(response http.ResponseWriter, request *http.Request) {
	//	sample
	//	http://localhost:9090
	//	http://localhost:9090/?url_long=111&url_long=222
	request.ParseForm()											//解析参数
	fmt.Println(request.Form)									//表单
	fmt.Println("path	", request.URL.Path)				//路由地址
	fmt.Println("scheme	",request.URL.Scheme)			//携带参数
	fmt.Println(request.Form["url_long"])
	for k,v := range request.Form{								//循环输出
		fmt.Println("key	",k)
		fmt.Println("value	",v)
	}
	fmt.Fprintf(response,"hello go lang! ")
}

```

### 3.2 表单

- 表单方法
``` go
func login(response http.ResponseWriter, request *http.Request) {
	fmt.Println("method	", request.Method)
	if request.Method == "GET" {
		t, _ := template.ParseFiles("login.gtpl")
		log.Println(t.Execute(response, nil))
	} else {
		request.ParseForm()
		fmt.Println("username	", request.Form["username"])
		fmt.Println("password	", request.Form["password"])
	}
}

```
- 字段解析 正则表达式 略

- 防止跨站攻击
``` go 
fmt.Println("username ",template.HTMLEscapeString(request.Form.Get("username")))
fmt.Println("password ",template.HTMLEscapeString(request.Form.Get("password")))
template.HTMLEscape(response,[]byte(request.Form.Get("username")))
```

- 防止多次递交表单

    增加token生成和检测，在gtpl中增加token的隐藏字段
``` go
func login(response http.ResponseWriter, request *http.Request) {
	fmt.Println("method	", request.Method)
	if request.Method == "GET" {
		currtime := time.Now().Unix()
		h := md5.New()
		io.WriteString(h, strconv.FormatInt(currtime,10))
		token := fmt.Sprintf("%x",h.Sum(nil))
		t, _ := template.ParseFiles("login.gtpl")
		log.Println(t.Execute(response, token))
	} else {
		request.ParseForm()
		//防止跨域攻击
		token :=request.Form.Get("token")
		if token !=""{
			//test token
			fmt.Println("token", token)
		}	else{
			// invalid !
			fmt.Println("no token")
		}
		fmt.Println("username ",template.HTMLEscapeString(request.Form.Get("username")))
		fmt.Println("password ",template.HTMLEscapeString(request.Form.Get("password")))
		template.HTMLEscape(response,[]byte(request.Form.Get("username")))
	}
}
```

- 处理文件上传

    - 为表单增加属性， enctype="multipart/form-data"
    - 表单处理的实现
    关键函数 ： request.ParseMultipartForm， 
    f,err := os.OpenFile("./test/"+handler.Filename,os.O_WRONLY|os.O_CREATE,0666)
``` go 
func upload(response http.ResponseWriter, request *http.Request) {
	fmt.Println("method",request.Method)
	if request.Method =="GET"{
		currtime := time.Now().Unix()
		h:= md5.New()
		io.WriteString(h,strconv.FormatInt(currtime,10))
		token :=fmt.Sprintf("%x",h.Sum(nil))

		t,_ := template.ParseFiles("upload.gtpl")
		t.Execute(response,token)
	} else {
		request.ParseMultipartForm(32<<20)
		//表示最大传输大小，超出大小将转存到系统临时文件
		file,handler,err := request.FormFile("uploadfile")
		if err != nil{
			fmt.Println(err)
			return
		}
		defer file.Close()
		fmt.Fprintf(response,"%v", handler.Header)
		fmt.Println("current upload filename ",handler.Filename)
		f,err := os.OpenFile("./test/"+handler.Filename,os.O_WRONLY|os.O_CREATE,0666)
		if err != nil{
			fmt.Println("err 123",err)
			return
		}
		defer f.Close()
		io.Copy(f,file)
	}
}
```

- 客户端实现， 略