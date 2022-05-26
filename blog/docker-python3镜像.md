# docker制作python3 镜像

在公司仓库居然没有找到合适的python3基础镜像，决定自己做一个


### 获取基础镜像

```  bash
#查询可用的私有仓库IP
docker info    

# 查询仓库中是否包含centos镜像
curl http://registry-ip:5000/v2/_catalog | grep centos

# 查询centos 标签
curl http://registry-ip:5000/v2/xx/centos/tags/list 

# 下载镜像并标签给自己
docker pull xx/centos:7.5
docker tag xx/centos:7.5 xxx/centos:7.5
```

### 制作镜像

准备python3.7.4 的包， 保存到/home/xx/dev/centos-python3.7
``` bash
# 使用run 命令启动镜像，并挂载安装包的路径
docker run --rm  -it   -v /home/xx/dev/centos-python3.7:/ext_input  --entrypoint="/bin/bash" xx/centos:v7.5

# 现在yum可能仍然不可用，可以拷贝宿主机/etc/yum/repo.d 到 镜像对应位置
# 发现内部仍然无法使用yum， 在宿主机上ping 仓库域名，获取ip，直接修改到镜像内
# 目测yum 可用

# Python 编译环境及依赖库, 缺少依赖库后编译出的python可能缺少某些组件，如 setuptools, pip等
yum install gcc make -y
yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel  &&\
readline-devel tk-devel gdbm-devel db4-devel libcap-devel xz-devel kernel-devel libffi-devel

# 打开到安装包路径，执行解包， 配置，编译，安装
tar -zxvf Python-3.7.4.tgz
./configure --prefix=/python/python3
make
make install

# 检查python 安装路径下是否已包含python3, pip3, 并创建软连接
ln -s /python/python3/bin/python3 /usr/bin/python3 
ln -s /python/python3/bin/pip3 /usr/bin/pip3 

# 在内网环境下pip可能仍然不可使用， 配置下仓库地址
mkdir -p /root/.pip/
vi /root/.pip/pip.conf 
# 填写自己的仓库配置
```

按上述步骤已创建一个可用的python环境，还可以根据需要配置中文包等
``` bash
# 保存当前镜像，并推送到私有仓库
docker ps -a 获取当前执行镜像的id
docker commit xxxx /xxx/python3.7.4:v1
docker tag xxx/python3.7.4:v1 registry_ip:5000/xxx/python3.7.4:v1
```
### 使用镜像
现在拥有一个独立的python镜像，可以按以下配置创建app

Dockerfile
``` Dockerfile
FROM xxx/python3.7.4:v1

COPY requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt

WORKDIR /python/python3.7.4

```

执行指令
```  bash
# docker启动镜像必然覆盖/etc/hosts，访问镜像可能仍需要指定hosts列表
docker build -t zzz/app:v1 .  &&\
--add-host=xxx:xxx --add-host=xxx:xxx
```

