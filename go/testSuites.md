# go测试

go应用测试

## 1. testing

- 概念
  - 源码文件:小写xxx.go；测试文件:xxx_test.go; 测试函数 TestFuncName(xxx)
  - 指令 go test -v -cover  / go test -v -short -parallel 4  
  - 测试类型
    - 单元测试 *testing.T
    - 基准测试 *testing.B
    - 主函数 TestMain(*testing.M)
  - 实用函数
    - t.skip() 跳过当前测试
    - t.Parallel() 并行测试
    - t.Log()/ t.Logf()  日志输出
    - t.Error() == t.Fail() + t.Log()  标记失败，允许继续运行
    - t.Fatal() == t.FailNow() + t.log() 标记失败，停止函数
  - http测试
    - 使用包 net/http/httptest
  

- demo

``` go 

// test xxx_test.go
func TestFunc(t *testing.T) {
    // ...
}

// benchmark
func BenchmarkFunc(t *testing.B){
    for i :=0;i < b.N; i++{
        // ...
    }
}

// http
func TestHandleRequest(t * testing.T){
    mux := http.NewServeMux()
    mux.HandleFunc("/router", handleRequest)

    writer := httptest.NewRecorder()
    req, _ := http.NewRequest("GET", "/route/params",nil)
    mux.ServeHttp(writer,req)

    if writer.Code != 200{
        t.Error(writer.Code)
    }

    var post Post
    json.Unmarshal(writer.Body.Bytes(), &post)
    t.Logf("%#v \n", post)
}

//main
func TestMain(m *testing.M){
    setUp
    code := m.Run()
    tearDown()
    os.Exit(code)
}

// multi test cases
func TestAddTag(t *testing.T) {
	tests := []struct {
		Name      string
		State     int
		CreatedBy string
	}{
		{
			Name:      "哲学♂",
			State:     1,
			CreatedBy: "jim",
		},
		{
			Name:      "放松",
			State:     1,
			CreatedBy: "lee",
		},
		{
			Name:      "宅",
			State:     1,
			CreatedBy: "jim",
		},
	}

	for _, v := range tests {
		if err := AddTag(v.Name, v.State, v.CreatedBy); err != nil {
			t.Error(err)
		}
	}

}

```

## 2. Convey

- 安装
  - 工具 go get github.com/smartystreets/goconvey， bin: goconvey
  - 导入包  . "github.com/smartystreets/goconvey/convey"  
  - 使用web界面： goconvey; url http://localhost:8080

- demo

``` go
func TestLogin(t *testing.T) {
	Convey("Test Login", t, func() {
		Convey("Should Login", func() {
			username := "jimtest"
			pass := "pass@123"
			ret, uid := Login(username, pass)
			So(ret, ShouldBeTrue)
			So(uid, ShouldEqual, 11)
		})
		Convey("should Not Login", func() {
			username := "jimtest"
			pass := "xxxx"
			ret, _ := Login(username, pass)
			So(ret, ShouldBeFalse)
		})
	})
}
```