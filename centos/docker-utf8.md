### * Docker解决中文乱码实践

- 问题
  
在公司使用dockers镜像中遇到一个问题，同事的python代码中使用 xx_str.encode('utf-8')在包含中文路径时报出异常，但在开发环境中没有遇到。

ps. 在开发中不要使用中文传递参数

- 排查步骤

``` bash
# 分别在开发环境和docker容器中执行 
locale -a

# 可以查看到docker环境仅包含posix编码，开发环境包括utf-8

# 调用python命令行执行：
sys.getdefaultencoding()
# 也可以发现两者的区别
```

- 尝试解决

由于同事无法直接提供Dockerfile，只能在他的镜像基础上做修改，
制作如下的Dockerfile

``` Dockerfile
FROM XXX # 同事的镜像名

RUN yum install kde-l10n-Chinese -y &&\
    yum reinstall glibc-common -y &&\
    localedef -c -f UTF-8 -i zh_CN zh_CN.utf8

ENV LANG zh_CN.UTF-8

WORKDIR /home/xxxx # 指定原先的工作路径

COPY run.sh . #新增一个启动脚本

EXPOSE 8080

ENTRYPOINT ["/bin/bash","run.sh"]
```

安装步骤
``` bash
docker build -t xxx #创建新镜像
docker run -d --rm xxx -p 10081:8080 xxx # 启动镜像
docker ps -a | grep xxx # 查找执行容器
docker exec -it xxxx bash # 到容器执行控制台
locale -a # 查看当前系统编码, 修改为zh_CN.utf-8
```


#### 参考

- [csdn](https://blog.csdn.net/hnmpf/article/details/81478972)