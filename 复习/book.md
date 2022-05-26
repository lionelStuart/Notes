# 1. book list
- The Art of Monitoring


# 2. 普罗米修斯

- 关联
  - tsdb
  - promql
  - 集群部署
    - 功能扩展
      - 按组织、地理位置、逻辑分区
    - 水平扩展
      - prom级联金字塔
  - node exporter 服务发现 DNS SRV记录
  - k8s cadvisr
  - 自定义指标、日志监控

# 3.kafka
- 优化设计
  - 页缓存，使用系统自带的page cache作为内存与磁盘间的cache机制。kafka消息队列应用场景的特殊性，即任务队列为顺序读写，远多余随机读写，可以直接利用系统自带的页缓存进行消息的落盘和读写
  - 零拷贝，socket读buffer从page cache直接读写，减少buffe转buffer的消耗。

减少数据共享和操作数据总线的次数。DMA。mmap。sendfile。sendfile系统调用利用DMA引擎将文件内容拷贝到内核缓冲区去，然后将带有文件位置和长度信息的缓冲区描述符添加socket缓冲区去，这一步不会将内核中的数据拷贝到socket缓冲区中，DMA引擎会将内核缓冲区的数据拷贝到协议引擎中去，避免了最后一次拷贝。

- 消息结构
  - topic-paration-message
  - paration没有多余业务含义，只提供吞吐
  - 生产端位移和消费端位移
  - <topic, paration, offsest> 与消息对应唯一

- ISR备份机制

- 场景
  - 信息收集
  - 日志收集

- producer
  - acks ， 1=leader ack， -1，all=isr ack
  - 

- customer
  - offset
    - 最多一次，可能丢失
    - 最少一次，不会丢失，但可能处理多次，默认
    - 精确一次，一定处理一次
    - 自动递交

  - 事务和幂等性



## BUG FIX

#### 1.1 重启主机eth0 丢失
- ifconfig eth0 up 重启可以成功
- ifconfig -a 可以看到未加载的eth0
- 网上检查网路填写正确

``` sh
# vi /etc/sysconfig/network-scripts/ifcfg-eth0
DEVICE="eth0"

HWADDR="00:0C:29:FC:1C:72"

NM_CONTROLLED="yes"

ONBOOT="yes"

```

- service network restart 命令重启会失败

按照以下操作可以恢复 network和NetsManager的冲突
``` sh
chkconfig NetworkManager off             #关闭NetworkManager随系统启动
service network restart                  # 重启网络服务 
chkconfig network on 
```

- /etc/udev/rules.d/70-persistent-net.rules

#### 1.2 使用fdisk扩展磁盘
- 需要使用root
- fdisk -l

#### 1.3 docker&minkube
- 使用官方非root docker
- 重启docker 使用 su - && service docker restart
- 检查docker docker version && docker run hello-world
-  使用阿里云镜像加速器 https://cr.console.aliyun.com/cn-hangzhou/instances/mirrors
-  dockerd-rootless-setuptool.sh install -f
- sudo docker
-  sudo minikube start
-  
minikube start --vm-driver=none --image-repository='registry.cn-hangzhou.aliyuncs.com/google_containers'source ~/.bashrx

- export KUBECONFIG=/etc/kubernetes/admin.conf


