
### 1.1 mysql 配置

1. 使用绿色版mysql,创建data文件夹，bin目录加入到path

2. 安装：
··· bat
mysqld -install /-remove

mysqld --initialize-insecure --user=mysql --explicit_defaults_for_timestamp

net start mysql /stop mysql

···

3. 初次登陆s

    修改ini文件配置路径，配置utf-8
``` bat
mysql -uroot -p   [ENTER]
mysqld restart
show variables like 'character%'

update user set authentication_string=PASSWORD("123456") where user="root";
flush privileges; 
quit;

use mysql;  # neon1234 root

```

4. 