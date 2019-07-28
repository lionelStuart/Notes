#### 1.1 http 客户端 

1. Client

``` go
//resp Get Methods
resp,err:=http.Get(url)
defer resp.Body().Close()

//resp param
for k,v :=range resp.Header{
    fmt.Printf('k=%v, v=%v\n',k,v)
}

// resp struct
fmt.Print(resp.Status,resp.StatusCode,resp.Proto,resp.ContentLength,resp.TransferEncoding,
resp.Uncompressed,
reflect.TypeOf(resp.Body()))

//request Do
req,err := http.NewRequest("POST",url)
req.Header.Set("Content-Type","application/json")
resp,err := client.Do(req)
defer resp.Body().Close()

//post form
//http.Post()
//http.PostForm()

postParam := url.Values{
    "mobile":{"xx"},
    "isRemembered":{"123"},
}
resp,err := http.PostForm(url,postParam)
defer resp.Body().CLose()
body,err := ioutil.ReadAll(resp.Body)
fmt.Println(string(body))


 ```


#### 1.2 服务端方法

1. ServeMux & Handler
    type Handler func(http.ResponseWriter, *http.Request)
    type ServeMux

``` go
mux := http.NewServeMux()

rh :=http.RedirectHandler(url,307)
mux.Handle(url, rh)

http.ListenAndServe(":3000",mux)

```

2. 自定义处理器

``` go
//1
type timeHandler struct{

}

func (th * timeHandler) ServeHttp(w http.ResponseWriter, r *http.Request){

}


mux := http.NewServeMux()
th := &timeHandler{}
mux.handle(url,th)
mux.Handle(":3000",mux)

//2
func timeHandler(w http.ResponseWriter, r* http.Request){

}

mux := http.NewServeMux()
th := http.HandlerFunc(timeHandler)
mux.handle(url,th)
mux.Handle(":3000",mux)

//3 闭包

func timeHandler() http.Handler {
    fn := func(w http.ResponseWriter, r* http.Request){

    }
    return http.HandlerFunc(fn)
}

func timeHandler() http.handler{
    return http.HandlerFunc(
        func(w http.ResponseWriter, r*http.Request){

        }        
    )
}

func timeHandler() http.handleFunc{
    return func(w http.ResponseWriter , r* http.Request){

    }
}

//4 defaultServeMux
func timeHandler(format string) http.Handler{
    fn := func(w http.ResponseWriter, r* http.Request){
        tm := time.Now().Format(format)
        w.Writer([]byte("time is "+tm))
    }
    return http.handlerFunc(fn)
}

th := timeHandler(time.RFC1123)
http.Handle("/time",th)
http.ListenAndServe(":3000",nil)
// nil 使用defaultServeMux



```

