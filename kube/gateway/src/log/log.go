package log

import (
	"os"

	"go.elastic.co/ecszap"
	"go.uber.org/zap"
)

var logger *zap.Logger

func Logger() *zap.Logger {
	return logger
}

func Init() {
	encoderConfig := ecszap.NewDefaultEncoderConfig()
	core := ecszap.NewCore(encoderConfig, os.Stdout, zap.DebugLevel)
	logger = zap.New(core, zap.AddCaller())
	logger = logger.With(zap.String("app", "gogo-gateway")).With(zap.String("env", "dev"))
}
