package main

import (
	"context"
	"fmt"
	"go.uber.org/zap"
	"os"
	"os/signal"
	"sample/log"
	sev "sample/server"
	"syscall"
	"time"
)

func startServer() {
	m := &sev.Server{}
	m.Start()
}

func main() {
	log.Init()

	ctx, cancel := context.WithCancel(context.Background())

	go func(context.Context) {
		tk := time.NewTicker(time.Second * 3)
		for {
			select {
			case <-ctx.Done():
				fmt.Println("Killed")
				return
			case <-tk.C:
				fmt.Printf("Echo Time Now:%#v\n", time.Now().Format(time.DateTime))
				log.Logger().Debug("Run In Loop time", zap.String("time", time.Now().Format(time.DateTime)))
			}
		}
	}(ctx)

	go func() {
		startServer()
	}()

	c := make(chan os.Signal)
	signal.Notify(c, syscall.SIGHUP, syscall.SIGINT, syscall.SIGTERM,
		syscall.SIGQUIT, syscall.SIGUSR1, syscall.SIGUSR2)
	<-c
	cancel()
	fmt.Println("Exit..")
	time.Sleep(time.Second)
	os.Exit(0)
}
