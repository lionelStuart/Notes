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


## 事务
1. RR级别死锁
- 两个事务同时做更新，更新行顺序不同
- insert加锁为正无穷大，修改为insert into on duplicate key update
- 在另外一个事务加间隙锁时，访问到其加间隙锁区间的记录锁
- 对加唯一索引的数据执行删除，会加间隙锁
- RR级别会加间隙锁，更容易出现死锁现象，所以线上一般使用RC级别
- 间隙锁可以共存，也就是加间隙锁可能死锁的原因


2. RC级别死锁
- RC级别下在insert下会使用GAP锁检测重复键
- RC 隔离级别相较 RR 隔离级别产生死锁的概率小，但仍不可避免。
- INSERT ... ON DUPLICATE KEY UPDATE 比 REPLACE 产生死锁的几率小且更安全高效。
- 并发事务按照相同的顺序处理数据。
- 事务尽快提交，避免大事务、长事务。

3. 间隙锁
- 间隙锁出现在能解决幻读的场景下
- RC相比RR减少间隙锁加锁机会，能降低加锁风险，提高并发，但对插入语句，仍会用间隙锁检测相同主键
