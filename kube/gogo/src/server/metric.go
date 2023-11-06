package server

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"math/rand"
	"sample/tracer"
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

	r := gin.Default()
	tracer.Init(r)
	vi := &VisitController{}
	vi.Init()
	defer vi.UnInit()
	r.GET("/resource", func(c *gin.Context) {
		now := time.Now().Format(time.DateTime)

		id := rand.Intn(10)
		vi.Add(id)

		c.JSON(200, gin.H{
			"message": fmt.Sprintf("recv message on %s", now),
			"status":  "ok",
		})
	})
	r.GET("/metrics", gin.WrapH(promhttp.Handler()))

	err := r.Run(":8080")
	if err != nil {
		return
	} // listen and serve on 0.0.0.0:8080

}
