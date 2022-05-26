# docker 

docker 部署应用

## 1. docker 部署web应用

- 编辑简单的文件服务器

``` go
package main

import (
	"fmt"docker
	"net/http"
	"os"
	"path"
	"path/filepath"
)

func main() {
	p, _ :=  filepath.Abs(filepath.Dir(os.Args[0]))
	p = path.Join(p,"static")
	http.Handle("/", http.FileServer(http.Dir(p)))
	err := http.ListenAndServe(":8088", nil)
	if err != nil {
		fmt.Println(err)
	}
}

```
- 工程配置

使用go build 编译为可执行文件main, 监听端口为8088， 文件夹目录为 static,建立目录格式如下：

```
-.
|--Dockerfile
|--main
|--static
|--run.sh
```

run.sh
``` bash
#! /usr/bin/env bash
cd /app && ./main
# 打开到app 目录并执行程序
```

- 生成镜像

配置运行目录为/app，暴露端口号8088， 执行CMD指令bash run.sh

Dockerfile
```
FROM golang
MAINTAINER jim
WORKDIR /app
COPY . .
EXPOSE 8088
CMD ["/bin/bash", "/app/run.sh"]
```
在当前目录生成docker镜像，使用docker images 查看生成的镜像
```
docker build -t go-web .
```

- 启动镜像

使用指令启动指令， --rm 在结束运行后删除 -d 在后台执行 -p 暴露本机端口给8088 -v 暴露本机完整路径给/app/static  指定名称为go-web1  
``` bash
docker run -d  --rm -p 8088:8088 -v /home/phoenix/workspace/static:/app/static  --name=go-web1  go-web

curl http://localhost:8088 
# 查看static 目录

docker exec -it xxxx bash 
# 在镜像中执行命令行
```

## 2. docker-compose

- 部署-demo1

static-compose.yml
```yml
version: '2'		# 使用version2

networks:
 basic:            # 创建网络类型， docker network ls

services:
 web:                       # 服务名
   container_name: web_app  # 镜像名
   image: go-web:v0.1       # 镜像地址
   ports:
    - "8089:8088"
   volumes:
    - /home/phoenix/workspace/static:/app/static:rw
   networks:
    - basic

```

启动指令
``` bash
docker-compose -f static-compose.yml up -d web
# 使用文件名发布服务后台启动
docker ps
```

- 部署多应用

``` yml
services:
 web1:
   container_name: web_c1
   image: go-web:v0.1
   ports:
    - "8089:8088"
   volumes:
    - /home/phoenix/workspace/gowork/staticFile/static:/app/static:rw
   networks:
    - basic
 web2:
   container_name: web_c2
   image: go-web:v0.1
   ports:
    - "8090:8088"
   volumes:
    - /home/phoenix/workspace/gowork/staticFile/static:/app/static:rw
   networks:
    - basic
```

- docker-compose 水平扩展
  
docker-compose水平扩展限制在单机,不能指定镜像名，不能绑定端口

docker-compose.yml
``` yml
version: '3'
services:
  web:
    image: nginx

  redis:
    image: redis
```

使用指令
``` bash
docker-compose up --scale web=3 -d
```

使用负载均衡
```
version: '3'
services:
  web:
    image: nginx

  redis:
    image: redis
  lib: 
    image: dockercloud/haproxy 
    links: 
      - web 
    ports: 
      - 8080:80 
```

执行指令
``` bash
docker-compose -f static-compose.yml up
# 发布

docker-compose -f static-compose.yml ps
# 查看进程，有web_c1, web_c2 与docker ps -a 结果相同 
```


- 概念
  - 安装： pip3 install docker-compose
  
- 指令 docker-compose -f xxx.yml 操作指定的yml
  - up, 运行服务，docker-compose -f static-compose.yml up -d web
  - ps, 列出运行容器，docker-compose -f static-compose.yml ps
  - start/pause/stop/restart/down/logs/build 启动/暂停/停止/重启/卸载/日志/构建
  - kill/config 杀死/验证配置
  - run，在指定容器运行指令，docker-compose -f static-compose.yml run web bash
  - exec, 运行指令， docker-compose -f static-compose.yml exec web bash
  
- yml模板文件
  - 主要模块： service, networks
  - services.image 指定镜像，不存在时会拉取
  - services.build 除指定镜像外，可以使用Dockerfile 启动构建 [context, dockerfile]
  - services.container_name 镜像名称
  - services.depends_on 确定启动容器的依赖顺序
  - services.ports 映射端口
  - services.extra_hosts 添加额外/etc/hosts 记录
  - services.volumes 挂载卷
  - services.volumes_from 从其他服务挂载卷
  - services.expose 暴露端口，不映射主机，作为内部端口
  - services.links 链接到其他服务的容器
  - services.net 设置网络模式
  
demo 
``` yml
version: '2'
services:
  web:
    image: dockercloud/hello-world
    ports:
      - 8080
    networks:
      - front-tier
      - back-tier
 
  redis:
    image: redis
    links:
      - web
    networks:
      - back-tier
 
  lb:
    image: dockercloud/haproxy
    ports:
      - 80:80
    links:
      - web
    networks:
      - front-tier
      - back-tier
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
 
networks:
  front-tier:
    driver: bridge
  back-tier:
    driver: bridge
```

## 3. 使用 k8s 部署

- 创建持久卷和持久卷申明

pv
``` yml
apiVersion: v1
kind: PersistentVolume # 创建持久卷
metadata:
  name: static-pv  # pv名称
spec:
  capacity:
    storage: 1Gi # 定义大小和多个客户端挂载时的访问模式
  accessModes:
    - ReadWriteOnce      # 只可在一个节点上读写
    - ReadOnlyMany       # 可在多个节点只读
  persistentVolumeReclaimPolicy: Retain  # 删除pv时不删除卷中内容
  hostPath:
    path: /hosthome/phoenix/ext  # minikube 默认挂载 /hosthome

```

pvc
``` yml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: static-web-pvc  # pvc名称
spec:
  resources:
    requests:
      storage: 1Gi
  accessModes:
    - ReadWriteOnce
  storageClassName: ""

```

- 申明部署 deployment

deployment
``` yml

apiVersion: extensions/v1beta1
kind: Deployment  # 类型为deployment
metadata:
  name: goapp-deploy
  labels:
    app: web-app
spec:
  replicas: 2     # pod=2
  revisionHistoryLimit: 10
  minReadySeconds: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
  template:
    metadata:
      labels:
        app: web-app
    spec:
      containers:
      - image: 192.168.0.240:5000/go-web:v0.2  # docker tag&push 的镜像
        imagePullPolicy: Always
        name: web-c  #容器名字
        volumeMounts:
        - name: mount-data   # 使用挂载卷的名字
          mountPath: /app/static   # 需要挂载的目录
          subPath: app      # 映射到挂载卷的子目录
        ports:
        - containerPort: 8080   # 需要开放的端口
          protocol: TCP
      volumes:
         - name: mount-data  # 使用挂载卷的名字
           persistentVolumeClaim:  #使用持久卷
            claimName: static-web-pvc  # pvc 申明
```

- 部署svc暴露服务

svc
``` yml
apiVersion: v1
kind: Service
metadata:
  name: web-svc-test
spec:
  type: NodePort  # 使用nodeport 暴露服务端口
  ports:
    - nodePort: 30010  # 提供给外部的服务端口 nodeip:port
      port: 80         # cluster 监听端口 在节点内部 clusterip:port
      targetPort: 8088  # 映射到的服务端口， pod-port
  selector:
    app: web-app   # 使用筛选器 label  app=web-app

```

- 调试，验证

``` bash
kubectl create -f xxxx 创建pv, pvc， deploy, svc

# 在minikube ssh中调试
kubectl get svc 获取cluster-ip
curl http://cluster-ip:80

# 在宿主机验证
minikube ip
curl http://node-ip:30010

```





#### 参考
- [简书](https://www.jianshu.com/p/5939dcf5c96e)
- [博客园](https://www.cnblogs.com/minseo/p/11548177.html)

