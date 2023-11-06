package server

import (
	"encoding/json"
	"github.com/IBM/sarama"
	"go.uber.org/zap"
	"os"
	"sample/log"
	"time"
)

var Account = []string{
	"John",
	"Mary",
	"James",
	"Jennifer",
	"Robert",
	"Elizabeth",
	"William",
	"Sarah",
	"Michael",
	"Emily",
}

type VisitController struct {
	p sarama.AsyncProducer
}

func (a *VisitController) Init() {
	config := sarama.NewConfig()
	config.Producer.Return.Successes = true
	config.Producer.Timeout = 30 * time.Second

	config.Producer.RequiredAcks = sarama.WaitForAll
	//随机向partition发送消息
	config.Producer.Partitioner = sarama.NewRandomPartitioner
	//是否等待成功和失败后的响应,只有上面的RequireAcks设置不是NoReponse这里才有用.
	config.Producer.Return.Successes = true
	config.Producer.Return.Errors = true
	//设置使用的kafka版本,如果低于V0_10_0_0版本,消息中的timestrap没有作用.需要消费和生产同时配置
	//注意，版本设置不对的话，kafka会返回很奇怪的错误，并且无法成功发送消息
	config.Version = sarama.V0_10_0_1

	kafkaAddr := os.Getenv("KAFKA_ADDR")
	//kafkaAddr = "127.0.0.1:30092"
	var err error
	a.p, err = sarama.NewAsyncProducer([]string{kafkaAddr}, config)
	if err != nil {
		log.Logger().Info("Fail init kafka", zap.Error(err))
	}

	go func(p sarama.AsyncProducer) {
		for {
			select {
			case <-p.Successes():
				//fmt.Println("offset: ", suc.Offset, "timestamp: ", suc.Timestamp.String(), "partitions: ", suc.Partition)
			case fail := <-p.Errors():
				log.Logger().Info("fail send message", zap.Error(fail))
			}
		}
	}(a.p)

}

func (a *VisitController) UnInit() {
	a.p.AsyncClose()
}

type Visit struct {
	Id      int
	Account string
	Time    string
}

func (a *VisitController) Add(id int) {
	if id > len(Account) {
		return
	}
	log.Logger().Debug("Visit Account:", zap.String("time", time.Now().Format(time.DateTime)),
		zap.String("visit", Account[id]))
	visit := &Visit{
		Id:      id,
		Account: Account[id],
		Time:    time.Now().Format(time.DateTime),
	}
	v, _ := json.Marshal(visit)

	a.p.Input() <- &sarama.ProducerMessage{
		Topic: "gogo-visit",
		Value: sarama.ByteEncoder(v),
	}
}
