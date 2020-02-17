# etcd

## 1. etcd

- 设置etcd版本
```
export ETCDCTL_API=3 
```
- etcdctl
  - etcdctl put foo bar 
  - etcdctl get foo  [--prefix]  [--limit] [--from-key]
  - etcdctl del foo foo9
  - etcdctl watch foo foo9
  - etcdctl lease grant(revoke) 10 /etcdctl put --lease=xx foo bar
  
## 2.etcd-api
- 故障

// 导入包 "github.com/coreos/etcd/clientv3"，后报错grpc中属性不存在，替换go.mod中的包

go.mod
```
require (
  github.com/coreos/etcd v3.3.18+incompatible
  github.com/coreos/go-systemd v0.0.0-00010101000000-000000000000 // indirect
)

replace (
	github.com/coreos/go-systemd => github.com/coreos/go-systemd/v22 v22.0.0
	google.golang.org/grpc => google.golang.org/grpc v1.26.0
)
```


#### 参考

- [etcd中文文档](https://doczhcn.gitbook.io/etcd/index)
