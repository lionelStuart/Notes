# linux cheatsheet

## 1.安装准备

#### 1.1 挂载磁盘

```
mkdir /data 
vi /etc/fstab

/dev/sdb1 /home ext4 defaults 1 2
```

#### 1.2 关闭防火墙

```
systemctl stop firewaalld.service
systemctl disable firewalld.service

# selinux 
setenforce 0
/etc/selinux/config
selinux=disabled

```

#### 1.3 ssh

```
systemctl start sshd
systemctl enable sshd
systemctl status sshd

```

#### 1.4 静态ip

```
地址    192.168.0.240
子网    255.255.255.0
网关    192.168.0.1
```

#### 1.5 安装golang

```
tar -xvf xx ... /home/phoenix/opt/go
vi /etc/profile
export GOROOT=/data/work/go
export GOPATH=/data/work/gopath
export PATH=$PATH:$GOROOT/bin:$GOPATH/bin

```

#### 1.6 docker

- install

```
sudo yum install -y yum-utils device-mapper-persistent-data lvm2 
yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo 
yum install docker-ce

sudo systemctl enable docker
sudo systemctl start docker

# exit
sudo groupadd docker
sudo usermod -aG docker $USER


```

- errors
  - PULL timeout
  ```
  vi /etc/docker/daemon.json
    {
  "registry-mirrors": ["https://registry.docker-cn.com"]
  } 

  dig @114.114.114.114 registry-1.docker.io
  
  vi /etc/hosts
  34.228.211.243 registry-1.docker.io

  sudo systemctl daemon-reload
  sudo systemctl restart docker
  docker info
  docker pull hello-world

  ``` 


#### 1.7 vi 

```
# 插入模式
i       当前位置插入
I       当前行首插入
o       下一行插入
O       上一行插入
a/A     追加/追加行尾


# 光标定位
G       最后一行
nG      第n行
$       当前行尾
^       当前行首
h,j,k,l 上下左右
:n      移动到


# 复制模式
yy      拷贝本行
p       粘贴


# 查找
/str    查找字符
n       正向移动
N       反向移动


# 撤销重做
u       撤销
.       重做


## 退出
ZZ     存盘
ZQ     不存盘
:q  /:wq    /:q!

```

#### 1.7信号

```
SIGHUP      1           用户终端结束，或守护进程重读配置
SIGPIPE                 写入关闭的管道或socket
SIGINT      2           ctrl+c
SIGKILL     9           强杀进程
SIGTERM     15          正常终止


kill        杀死pid
pkill       匹配杀死


cmd&            后台执行
nohup cmd&      注销可用
jobs            显示工作
```

#### 1.8 windows Linuxz子环境 （WSL）
- 开启开发者模式，程序 >安装linux子系统
- windows stores >安装ubuntu
- 启动系统，创建用户名
- ssh配置
  - sudo vi /etc/ssh/sshd_config
  ```
    Port 2222
    PasswoedAuthentication yes
    ssh_host_key & ecdsa_key & ed:25519_key
  ```
  - sudo service ssh --full-restart
  - sudo service ssh start
  - 配置mobax, localhost:2222@username
 
#### 1.9 Tips
 - auth failure : sudo passwd root etc.

## 2.组件

#### 2.1 seaweed

```
# https://github.com/chrislusf/seaweedfs

# master & volume
weed master
sudo nohup ./weed master -mdir=/data/fileData -port=9333 -defaultReplication="001" -ip="ip地址" >>/data/fileData/server_sfs.log &

sudo ./weed volume -dir=/data/t_v1 -max=5 -mserver="ip地址:9333" -port=9080 -ip="ip地址" >>/data/t_v1_sfs.log &

sudo ./weed volume -dir=/data/t_v2 -max=5 -mserver="ip地址:9333" -port=9081 -ip="ip地址" >>/data/t_v2_sfs.log &

sudo ./weed volume -dir=/data/t_v3 -max=5 -mserver="ip地址:9333" -port=9082 -ip="ip地址" >>/data/t_v3_sfs.log &

# upload 
curl -X POST http://localhost:9333/dir/assign
curl -X PUT -F file=@/home/xxx  http://localhost:9080/xxx
curl -X DELETE
curl http://localhost:9333/dir/lookup?volumeId=xxx

# use docker 
```

## 3.k8s

#### 3.1 安装VirtualBox

- 没有硬件虚拟化，则需要安装
```
sudo yum install kernel-devel kernel-headers make patch gcc

sudo wget https://download.virtualbox.org/virtualbox/rpm/el/virtualbox.repo -P /etc/yum.repos.d

sudo yum install VirtualBox-5.2

# Ext
wget https://download.virtualbox.org/virtualbox/5.2.20/Oracle_VM_VirtualBox_Extension_Pack-5.2.20.vbox-extpack

sudo VBoxManage extpack install  Oracle_VM_VirtualBox_Extension_Pack-5.2.20.vbox-extpack

# 验证
systemctl status vboxdrv

# url
https://www.linuxidc.com/Linux/2018-11/155220.htm
```



#### 3.2 安装minikube 

- 1.install

```
curl -Lo minikube http://kubernetes.oss-cn-hangzhou.aliyuncs.com/minikube/releases/v1.2.0/minikube-linux-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/

# start
minikube start --registry-mirror=https://registry.docker-cn.com 

# install kubectl 
curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.15.0/bin/linux/amd64/kubectl && chmod +x ./kubectl && sudo mv ./kubectl /usr/local/bin/kubectl

# install web ui
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0-beta1/aio/deploy/recommended.yaml

kubectl proxy

# open dashboard
minikube dashboard

```

- 2.local registry
  - registry
      * docker pull registry
      * docker run -d -p 5000:5000 -v $(pwd):/var/lib/registry --restart always --name registry registry:2
      * vi /etc/docker/daemon.json
        ```
        "insecure-registries":["192.168.0.240:5000"],
        ```
      * sudo systemctl daemon-reload && sudo systemctl restart docker
      * curl http://192.168.0.240:5000/v2/_catalog  
  - push 
      * docker tag hello-node:v1 192.168.0.240:5000/hello-node:v1
      * docker push 192.168.0.240:5000/hello-node:v1
      * curl http://192.168.0.240:5000/v2/_catalog  
  - insecure-registry
      * minikube delete && minikube start --insecure-registry=192.168.0.240:5000
      * kubectl run hello-node --image=192.168.0.240:5000/hello-node
      * kubectl get pods ,kubectl get deployments, kubectl get events
  
- 3.demo
  - create file
  
    **server.js**
    ``` js
      var http = require('http');

      var handleRequest = function(request, response) {
        console.log('Received request for URL: ' + request.url);
        response.writeHead(200);
        response.end('Hello World!');
      };
      var www = http.createServer(handleRequest);
      www.listen(8080);
    ```
    **Dockerfile**
    ``` Dockerfile
      FROM node:6.9.2
      EXPOSE 8080
      COPY server.js .
      CMD node server.js
    ```

  - build
    
    docker build -t hello-node:v1 .

    docker push 192.168.0.240:5000/hello-node:v1

  - deployment

    kubectl run hello-node --image=192.168.0.240:5000/hello-node:v1 --port=8080

    eval $(minikube docker-env)  // eval $(minikuebe docker-env -u)

    查看dep: kubectl get deployments

    查看pod: kubectl get pods

    查看events: kubectl get events

  - service

    kubectl expose deployment hello-node --type=LoadBalancer

    kubectl get services

    minikube service hello-node

  - 发布流程
    *  docker build -t name:tag .
    *  docker tag name:tag p:name:tag
    *  docker push p:name:tag
    *  kubectl run name --image=p:name:tag
      or： kubectl set image deployment/name name=p:name:tag
    * 清除 kubectl delete service name & kubectl delete deployment name

#### 3.3 

- docker cmd
  - docker images
  - docker build
  - docker push/ pull
  - docker rm/ rmi

- minikube cmd
  - minikube delete && minikube start 
  - minikube stop
  - minikube logs

- kubectl cmd
  - kubectl get pods /nodes /depolyments /events





