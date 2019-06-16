## 4. 数据库

### 4.1 概念

1. 没有实现官方驱动，但提供了接口实现
2. sql.Register 注册数据库驱动
    
    在init中执行驱动的注册
3. driver.Driver 定义数据库接口
     - open 用于返回数据库连接
4.  driver.Conn 数据库连接的接口定义
    - Prepare 返回sql执行状态，可进行查询和删除
    - Close 关闭当前连接，驱动实现了连接池
    - Begin 开启一个事务连接 Tx ,可通过事务进行查询和更新，回滚，递交
5.  driver.Stmt 与连接相关，只用于goroutine

    - Close 关闭连接状态，返回query 有效行
    - NumInput 返回预留参数的个数，或 -1
    - Exec 执行sql，传入insert/update，返回Result
    - Query 执行sql,传入select ，返回Rows

6. driver.Tx 事务提交或回滚，实现Commit 和 Rollback
7. driver.Execer 实现 Exec
8. driver.Result 结果集定义，实现LasetInsertId,RowsAffected
9. driver.Rows 查询集定义，Columns/Close/Next
10. driver.RowsAffected == type:int64
11. driver.Value == interface{} 万能接口
12. driver.ValueConverter { ConvertValue  }
13. driver.sql
DB 结构,提供高阶接口，简化数据库操作，实现了连接池
``` go

type DB struct {
    driver   driver.Driver
    dsn      string
    mu       sync.Mutex // protects freeConn and closed
    freeConn []driver.Conn
    closed   bool
}

```

### 4.2 Mysql 数据库

repo： https://github.com/go-sql-driver/mysql 

