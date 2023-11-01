package main

import (
	"context"
	"fmt"
	"os"
	"os/signal"
	metric2 "sample/metric"
	"syscall"
	"time"
)

func metric() {
	m := &metric2.Server{}
	m.Start()
}

func main() {
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
			}
		}
	}(ctx)

	go func() {
		metric()
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
