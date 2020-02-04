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
#### 3.3 demo-1  

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

#### 3.6 demo-2

- 准备镜像
``` bash

docker pull nginx
docker tag nginx:latest 192.168.0.240:5000/nginx:latest
docker push 192.168.0.240:5000/nginx:latest
```

- 发布pod

nginxPod.yaml

``` yaml
apiVersion: v1
kind: Pod
metadata:
    name: nginx
    labels:
      app: nginx
spec:
    containers:
    - image: nginx
      name: nginx
      ports:
      - containerPort: 80
```
创建pod
``` bash
kubectl create -f nginxPod.yaml
kubectl get pod
```

- 发布服务

nginxService.yaml

``` yaml
apiVersion: v1
kind: Service
metadata:
    name: nginx
spec:
    type: LoadBalancer
    ports: 
    - port: 80
      targetPort: 80
    selector: 
      app: nginx
```

创建svc

```
kubectl create -f nginxService.yaml
kubectl get svc
```

- 查看发布

查询集群信息

``` bash
kubectl get nodes
kubectl describe node [nodeName] 显示InternalIP
# or
minikube ip

kubectl get svc 获取端口号
```
访问服务

``` bash
curl http://internalip:port
# or
minikube service [serviceName]
# or 
kubectl port-forward [service-Name] [Ip:Ip] 

```



#### 3.5 cheatsheet

- docker cmd
  - docker images
  - docker build
  - docker push/ pull
  - docker rm/ rmi
  - docker image inspect redis:latest | grep -i version 查看latest 版本
  - docker --exec -i name bash (into bash)
  - docker run --name= xxx-c  -p -d xxx / docker stop 
  - docker tag from  to

- minikube cmd
  - minikube delete && minikube start 
  - minikube stop
  - minikube logs

- kubectl cmd
  - kubectl get pods /nodes /depolyments /events
  - kubectl describe pod xxx
  - kubectl api-resources /shortname
  - kubectl get po/rc/rs/ev/deploy
  - kubectl get deploy kubia-1 -o yaml
  - 使用标签： kubectl label po xxx label=xxx [--overwrite] | kubectl get po -L xx,xx | kubectl get po -l xx=xx
  - 水平扩展: kubectl scale rc xx --replicas=10
  - 在容器中执行远程命令: kubectl exec [pod-name] -- [cmds]
  - configMap: kubectl create configmap xxx --from-literal=... | --from-file=... [path] | 

#### 3.6 概念
- ip
  
  NodeIp > clusterIp >  podIp
  clusterIp : cluster内部，pod可访问的ip


- 探针 Probe
``` yaml
libenessProbe:
  httpGet:
   path:
   port: 
  initialDelaySeconds:
  
```

``` bash
kubectl get po xxx
kubectl describe po xxx
```

- 控制器
  
  rc > rs > daemonSet > job > cronJob
  - rs: 相比rc, 增加了标签选择器，使所有标签与pod匹配为真
  - daemonset: 按给定的nodeSelector 在每个指定节点上运行一个pod
  - job: 按给定顺序、并行(completions, parallelism)执行一组后结束，重启不可为always

- svc
  - pod服务ip访问方式： 环境变量， DNS, FQDN
  ``` bash
  kubectl exec [pod-name] env
  kubectl exec -it [pod-name] bash
  curl http://name.default.svc.cluster.local
  curl http://kubia.default
  curl http://kubia
  ```
  - 连接外部服务

  手动指定ep kubectl get ep [svc] , 或
  ExternalName FQDN
  - 暴露服务
  - 
  NodePort, LoadBalance, Ingress 

-挂载

 - 类型
  
  emptyDir:  {}， medium: Memory | gitRepo | 

  持久类型： hostPath | GCE |
  PV | PVC 

- 配置
   - 类型

  args, env: name,value  

  configMap
