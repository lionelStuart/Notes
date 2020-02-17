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

- setup
	
	Convey可多层嵌套,，固没有配置setup。只有第一层Convey需要嵌入t
- teardown

	使用 Reset() {}

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

		Reset() {
			// do tear down
		}
	})
}
```

## 3. gomock

- 安装
  - 工具 go get github.com/golang/mock/gomock   mockgen
  - 指令 mockgen -source user.go -destination user_mock.go -package user

- demo

待测试打桩接口 
``` go
package user

type User struct {
	Name string
}

type UserRepository interface {
	Find(id int) (*User,error)
}


```
生成user_mock.go, 测试 user_test.go

``` go

func TestUserReturn(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	repo := NewMockUserRepository(ctrl)

	repo.EXPECT().Find(1).Return(&User{Name:"jim"},nil)
	repo.EXPECT().Find(2).Return(&User{Name:"marry"},nil)

	fmt.Println(repo.Find(1))
	fmt.Println(repo.Find(2))
	//fmt.Println(repo.Find(3))
}

func TestReturnDynamic(t *testing.T){
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	repo := NewMockUserRepository(ctrl)
	repo.EXPECT().Find(gomock.Any()).DoAndReturn(func(id int)(*User,error){
		if id ==0{
			return nil,errors.New("user not exist")
		}
		if id<100{
			return &User{
				Name:"LessUser",
			},nil
		} else {
			return &User{"LargeUser"},nil
		}
	})
	//t.Log(repo.Find(10))
	t.Log(repo.Find(110))
	//t.Log(repo.Find(0))

}

func TestTimes(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	repo := NewMockUserRepository(ctrl)
	// 默认期望调用一次
	repo.EXPECT().Find(1).Return(&User{Name: "张三"}, nil)
	// 期望调用2次
	repo.EXPECT().Find(2).Return(&User{Name: "李四"}, nil).Times(2)
	// 调用多少次可以,包括0次
	repo.EXPECT().Find(3).Return(nil, errors.New("user not found")).AnyTimes()

	// 验证一下结果
	fmt.Println(repo.Find(1)) // 这是张三
	fmt.Println(repo.Find(2)) // 这是李四
	fmt.Println(repo.Find(2)) // FindOne(2) 需调用两次,注释本行代码将导致测试不通过
	fmt.Println(repo.Find(3)) // user not found, 不限调用次数，注释掉本行也能通过测试
}


func TestOrder(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()
	repo := NewMockUserRepository(ctrl)
	o1 := repo.EXPECT().Find(1).Return(&User{Name: "张三"}, nil)
	o2 := repo.EXPECT().Find(2).Return(&User{Name: "李四"}, nil)
	o3 := repo.EXPECT().Find(3).Return(nil, errors.New("user not found"))
	gomock.InOrder(o1, o2, o3) //设置调用顺序
	// 按顺序调用，验证一下结果
	fmt.Println(repo.Find(1)) // 这是张三
	fmt.Println(repo.Find(2)) // 这是李四
	fmt.Println(repo.Find(3)) // user not found

	// 如果我们调整了调用顺序，将导致测试不通过：
	// log.Println(repo.FindOne(2)) // 这是李四
	// log.Println(repo.FindOne(1)) // 这是张三
	// log.Println(repo.FindOne(3)) // user not found
}


```

#### 参考

- [简书](https://www.jianshu.com/p/5582ff72170a)