# Redis

## 摘要

- 面试题
    - redis与memcached差异
    - redis数据类型
    - redis线程模型、单线程处理的优势、为什么加入多线程
    - 持久化、RDB、AOF
    - 集群模式、主从、哨兵、切片集群
    - 脑裂解决方案、从节点数量&延迟
    - 惰性删除+定期删除
    - 内存淘汰策略、有过期时间、无过期时间
    - 缓存雪崩(容灾)、击穿(热key失效)、穿透(风控)
    - 缓存更新策略、旁路(Y)、RW Through、Write Back
    - 缓存和数据库一致性、旧数据更新(更新再删除)
    - 大key、unlink
    - redis 分布式锁、red lock