# -*- coding: utf8 -*-
__author__ = 'paul_leung'

import datetime, logging
from pyflink.table import EnvironmentSettings, TableEnvironment


class PyFlinkBasicOperations():
 def __init__(self, proc_mode):
 # 创建TableEnvironment对象
    env_settings = None
    if proc_mode == 'streaming':
                env_settings = EnvironmentSettings\
                    .new_instance()\
                    .in_streaming_mode()\
                    .build()
    self.table_env = TableEnvironment.create(env_settings)
    if proc_mode == 'batch':
                env_settings = EnvironmentSettings\
                    .new_instance()\
                    .in_batch_mode()\
                    .build()
    self.table_env = TableEnvironment.create(env_settings)

 def table_api_sql_demo(self):
   # 1. 以DDL方式定义源表source_tb
   self.table_env.execute_sql("""
            CREATE TABLE source_tb (
                id INT,
                data VARCHAR
            ) WITH (
                'connector' = 'datagen',
                'fields.id.kind' = 'sequence',
                'fields.id.start' = '1',
                'fields.id.end' = '10'
              )
           """)  # 这条DDL定义的是一个无界的数据表，只能用streaming_mode处理而不能用batch_mode

        # 2. 以DDL方式定义目标表sink_table
   self.table_env.execute_sql("""
        CREATE TABLE sink_table (
                id INT,
                data VARCHAR
        ) WITH (
            'connector' = 'print'
          )
        """)

   # 3. 处理源表中的数据
   result = self.table_env.sql_query(
       "select id + 2, '{}' from source_tb".format(datetime.datetime.utcnow())
   )
   # 4. 将处理后的结果数据发送到目标表
   result.execute_insert("sink_table").print()

   # 上面的 #3. 和 #4. 效果与下面这条语句一致
   # result = self.table_env.execute_sql(
        #     "INSERT INTO sink_table select id + 2, '{}' from source_tb".format(datetime.datetime.utcnow())
        # ).wait()


if __name__ == "__main__":
    basic = PyFlinkBasicOperations("streaming")
    basic.table_api_sql_demo()