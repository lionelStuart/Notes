package main

import (
	"context"
	"fmt"
	"testing"
	"time"
)

func customer(ctx context.Context, input chan int) {
	for {
		select {
		case <-ctx.Done():
			return
		case v := <-input:
			fmt.Println("cusomter recv,", v)
		}
	}
}

func producer(ctx context.Context, out chan int) {
	cnt := 0
	timer := time.NewTicker(time.Second)
	for {
		select {
		case <-timer.C:
			cnt += 1
			out <- cnt
		case <-ctx.Done():
			return
		}
	}
}

func TestProducer(t *testing.T) {
	fmt.Println("test")
	ctx := context.Background()
	ch := make(chan int)
	go customer(ctx, ch)
	go producer(ctx, ch)
	select {}
}
