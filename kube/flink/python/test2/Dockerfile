FROM openjdk:11.0.11-jdk-slim

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN sed -i "s@http://deb.debian.org@http://mirrors.aliyun.com@g" /etc/apt/sources.list && \
    cat /etc/apt/sources.list && \
    rm -Rf /var/lib/apt/lists/* && apt-get update
RUN apt-get install -y python3 python3-pip 

RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip3 install apache-flink==1.16.0


# fail

