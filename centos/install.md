## 安装准备

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
