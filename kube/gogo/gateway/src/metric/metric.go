package metric

import "net/http"

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
	http.Handle("/metrics", promhttp.Handler())
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		return
	}
}
