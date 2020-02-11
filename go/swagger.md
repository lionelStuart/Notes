# swagger 使用

## 安装
- 命令行工具

``` bash
go get github.com/swaggo/swag/cmd/swag
# 安装到$GOPATH/bin下
# 使用指令 swag
```

- 安装依赖包

注入到router.go中

``` go
import (

	_ "sisyphus/docs"          // 自动生成swag文件位置
	"github.com/swaggo/gin-swagger"
	"github.com/swaggo/gin-swagger/swaggerFiles"
)

// 使用gin路由 gin.engine

engine.GET("/swagger/*any",ginSwagger.WrapHandler(swaggerFiles.Handler))

```

- 编写注释
``` go

// @title Golang 
// @version 1.0
// @description An example
// @termsOfService https://github.com/
// @license.name MIT
// @license.url https://github.com//LICENSE
func main(){
  ...
}


// @Summary Get multiple article tags
// @Produce  json
// @Param name query string false "Name"
// @Param state query int false "State"
// @Success 200 {object} app.Response
// @Failure 500 {object} app.Response
// @Router /api/v1/tags [get]
func GetTag(c*gign.Context){
  ...
}
```

- 生成并访问
``` bash
swag init
go run main.go

//web: http://127.0.0.1:8080/swagger/index.html
```