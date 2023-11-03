## 存储

- 静态存储卷和动态存储卷

人为定义PV、PVC的方式为静态卷。定义StorageClass，创建PVC动态申领PV是动态存储卷，需要插件支持

Local PV 
解决hostPath不好用的问题，定义PV时需要节点亲和性