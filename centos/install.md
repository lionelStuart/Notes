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
ps -ef          显示后台
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

#### 1.10 shell

- 查找
  - find / -name 万能， 遍历查找
  - locate 从数据库索引查找，可模糊匹配,需要updatedb
  - which 查找path中的可执行文件
  - whereis 按名字查找二进制，源文件，需要updatedb

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







