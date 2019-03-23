
# Spark

## 1.1集群部署

-   解压安装包到module文件夹
-   配置文件
    - 拷贝slaves.template为slaves
    - 拷贝spark-env.sh.temlate到spark-env.sh

``` bash
# slaves
host-slave..

#env.sh
SPARK_MASTER_HOST=master01
SPARK_MASTER_PORT=7077
```
- 启动
  - xsync安装包到其它机器
  - 在master上使用sbin/start-all.sh
  - jps可见master/worker; web登陆had001:8080  


- 启用history-server
  - 拷贝spark-defaults.conf.template为spark-defaults.conf
  - 启用sbin/start-history-server.sh
  - 查看端口开启服务 had002:7078

``` bash
# 修改conf
## 主机地址 
spark.master                     spark://had002:7077
## 开启日志
spark.eventLog.enabled           true
## hdfs文件夹位置
## 需要手工创建 hdfs dfs -mkdir /directory
spark.eventLog.dir               hdfs://had002:9000/directory

## 修改spark-env.sh
# 指定访问端口 指定记录路径 备份内存备份数目 
export SPARK_HISTORY_OPTS="-Dspark.history.ui.port=7077
-Dspark.history.retainedApplications=3
-Dspark.history.fs.logDirectory=hdfs://had002:9000/directory"

#指定hadoop——lib位置
export LD_LIBRARY_PATH=$HADOOP_HOME/lib/native

```

## 1.2 wordCount
-   spark shell
    - conf/pro4j 修改日志级别
    - dfs操作
      - bin/hdfs dfs -put ./README.txt /
      - dfs -ls /
      - dfs -cat/out/part-00000
    - spark shell
``` bash
sc.textFile("hdfs://had002:9000/README.txt").flatMap(_.split(" ")).map((_,1)).reduceByKey(_+_).saveAsTextFile("hdfs://had002:9000/out")
```

- scala api 

  - 编码
``` scala
object wordCount{
    val logger = LoggerFactory.getLogger(wordCount.getClass)

    def main(args:Array[string]){
        val conf = sparkConf().setAppName("wc")
        val sc = new sparkContext(conf)

        sc.textFile(args(0)).flatMap(_.split(" ")).map((_,1)).reduceByKey(
            _+_,1).sortBy(_._2,false).saveAsTextFile(args(1))
        
        logger.info("complete!)

        sc.stop()
    }
}
```

- 提交应用
``` bash
/bin/spark/spark-submit\
--class com.test.spark.WordCount \
--master spark://had002:7077 \
--executor-memory 1G \
--total-executor-cores 2 \
wordcount-jar-with-dependencies.jar \
hdfs://had002:9000/RELEASE \
hdfs://had002:9000/out
```

## 1.3 spark Idea
- 尝试N次后，放弃用maven构建spark工程，改用gradle
- 下载与spark等同版本的scala包，指定global lib scala spark/jars
- idea安装scala插件
- idea指定gradle/bin 本地路径
- 本地建立gradle项目，不勾选模板
- 编辑gradle文件, 指定rep 及依赖项

``` gradle
plugins {
    id 'java'
}

group 'com.phoenix'
version '1.0-SNAPSHOT'

sourceCompatibility = 1.8

repositories {
    maven {
        url 'http://maven.aliyun.com/nexus/content/groups/public/'
    }
    mavenCentral()

}

dependencies {
    testCompile group: 'junit', name: 'junit', version: '4.11'
    compile group: 'org.scala-lang', name: 'scala-library', version: '2.11.12'
    testCompile "org.scala-lang:scala-library:2.11.12"
    compile group: 'org.apache.spark', name: 'spark-core_2.11', version: '2.4.10'

}
```

- 编码 

``` scala
import org.apache.spark.{SparkConf, SparkContext}
import org.slf4j.LoggerFactory

object wordCount {
  val logger = LoggerFactory.getLogger(wordCount.getClass)

  def main(args: Array[String]){
    val conf = new SparkConf().setAppName("WC")
    val sc = new SparkContext(conf)


    sc.textFile(args(0)).flatMap(_.split(" "))
      .map((_, 1)).reduceByKey(_ + _, 1)
      .sortBy(_._2, false).saveAsTextFile(args(1))

    logger.info("complete")
    sc.stop()
  }
}

```

- spark-submit

``` bash
 bin/spark-submit --class wordCount \
> /opt/test/sparkdemo-0.3.jar \
> hdfs://had002:9000/README.txt \
> hdfs://had002:9000/out2
```

