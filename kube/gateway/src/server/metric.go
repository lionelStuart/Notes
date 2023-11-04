package server

import (
	"fmt"
	"gateway/log"
	"gateway/tracer"
	"github.com/SkyAPM/go2sky"
	httpPlugin "github.com/SkyAPM/go2sky/plugins/http"
	"github.com/gin-gonic/gin"
	"go.uber.org/zap"
	"io"
	"net/http"
	"os"
	"time"
)

import (
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

type Server struct {
}

func (m *Server) Start() {
	// 定义指标
	cpuUsage := prometheus.NewGauge(prometheus.GaugeOpts{
		Name: "cpu_usage",                      // 指标名称
		Help: "this is test metrics cpu usage", // 帮助信息

	})
	// 给指标设置值
	cpuUsage.Set(29.56)
	// 注册指标
	prometheus.MustRegister(cpuUsage)
	// 暴露指标

	addr := os.Getenv("GOGO_ADDR")

	r := gin.Default()
	tracer.Init(r)
	//r.Use(tracer.GinTraceMId)

	r.GET("/search", func(c *gin.Context) {
		now := time.Now().Format(time.DateTime)
		cli, err := httpPlugin.NewClient(go2sky.GetGlobalTracer())
		if err != nil {
			log.Logger().Fatal("get global tracer error \n", zap.Error(err))
		}

		req, err := http.NewRequest("GET", fmt.Sprintf("http://%s/resource", addr), nil)
		if err != nil {
			c.JSON(200, gin.H{
				"message": "fail",
				"status":  "bad",
			})
		}
		resp, err := cli.Do(req)
		if err != nil {
			log.Logger().Fatal("request error \n", zap.Error(err))
			c.JSON(200, gin.H{
				"message": "fail",
				"status":  "bad",
			})
			return
		}

		// 处理HTTP响应
		defer func(Body io.ReadCloser) {
			err := Body.Close()
			if err != nil {
				c.JSON(200, gin.H{
					"message": "fail",
					"status":  "bad",
				})
			}
		}(resp.Body)

		body, err := io.ReadAll(resp.Body)
		if err != nil {
			panic(err)
		}

		log.Logger().Info("request downstream success \n", zap.String("time", time.Now().Format(time.DateTime)))

		c.JSON(200, gin.H{
			"message": fmt.Sprintf("recv message on %s, got=%s", now, string(body)),
			"status":  "ok",
		})
	})
	r.GET("/metrics", gin.WrapH(promhttp.Handler()))

	err := r.Run(":8090")
	if err != nil {
		return
	} // listen and serve on 0.0.0.0:8080

}
