package tracer

import (
	"github.com/gin-gonic/gin"
	"go.uber.org/zap"
	"os"
	"sample/log"
)
import (
	"github.com/SkyAPM/go2sky"
	v3 "github.com/SkyAPM/go2sky-plugins/gin/v3"
	"github.com/SkyAPM/go2sky/reporter"
)

var GinTraceMId gin.HandlerFunc

func Init(e *gin.Engine) {
	skyAddr := os.Getenv("SKY_ADDR")

	grpcReporter, err := reporter.NewGRPCReporter(skyAddr)
	if err != nil {
		log.Logger().Fatal("new grpcReporter error \n", zap.Error(err))
		return
	}
	tracer, err := go2sky.NewTracer("gogo-api", go2sky.WithReporter(grpcReporter))
	if err != nil {
		log.Logger().Fatal("create tracer error \n", zap.Error(err))
	}

	go2sky.SetGlobalTracer(tracer)

	GinTraceMId = v3.Middleware(e, go2sky.GetGlobalTracer())
	if err != nil {
		log.Logger().Fatal("create middleware error \n", zap.Error(err))
	}
	e.Use(GinTraceMId)
}
