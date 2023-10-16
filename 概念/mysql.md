# 数据库

## 摘要
```
参考小林coding
```
- 索引
    - 主键索引、二级索引
    - b+树与b树的区别、特点、vs Hash、二叉树
    - 回表
    - 覆盖索引、索引下推
    - 联合索引、最左匹配、等值查询和范围查询、索引区分度
    - explain、show index on、desc
- 事务和锁
    - 事务隔离级别、脏读、不可重复读、幻读
    - redo log、undo log、bin log、MVCC
    - read view、update操作在RC和RR下的差异
    - next-key lock(记录锁+间隙锁) for update/share mode - 当前读(insert、update、delete)、快照读（普通select）
    - 不可避免的幻读场景(插入)：RR级别下未阻止插入、未立刻使用间隙锁
- 日志
    - buffer pool、LRU算法
    - undo、redo
    - redo log buffer、page cache、刷盘时机
    - innodb_flush_log_at_trx_commit
    - bin log、主从复制、复制模式、sync_binlog 
    - 2TC、双1配置




## 索引
1. 主键索引
- 一定会有主键索引

        如果有主键，默认会使用主键作为聚簇索引的索引键（key）；
        如果没有主键，就选择第一个不包含 NULL 值的唯一列作为聚簇索引的索引键（key）；
        在上面两个都没有的情况下，InnoDB 将自动生成一个隐式自增 id 列作为聚簇索引的索引键（key）；

- 其他索引都属于二级索引
