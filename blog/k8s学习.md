## 存储

- 静态存储卷和动态存储卷

人为定义PV、PVC的方式为静态卷。定义StorageClass，创建PVC动态申领PV是动态存储卷，需要插件支持

Local PV 
解决hostPath不好用的问题，定义PV时需要节点亲和性

## docker 原理

- cgroup(用量)+chroot(权限)+namespace(名字空间)=LXC
- LXC+AUFS(堆叠虚拟文件系统)=docker
- namespac限制资源可见性
- cgroup限制用量
- AUFS是逻辑目录
