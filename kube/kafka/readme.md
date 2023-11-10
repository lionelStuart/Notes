https://blog.csdn.net/Datura_qing/article/details/123003387


https://blog.csdn.net/tflasd1157/article/details/81985722


kafka-console-producer.sh --broker-list 127.0.0.1:9092 --topic demo



kafka-console-consumer.sh --bootstrap-server 127.0.0.1:9092  --topic demo --from-beginning


https://blog.csdn.net/Backpace_/article/details/120278064


docker run -d --name=zk-dev -p 2181:2181 -t wurstmeister/zookeeper


docker run  --name=zk-dev -p 2181:2181 -t wurstmeister/zookeeper

docker run  -d --name kafka-dev -p 19092:9092  --env KAFKA_ADVERTISED_HOST_NAME=127.0.0.1  -e KAFKA_ZOOKEEPER_CONNECT=127.0.0.1:2181 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://127.0.0.1:19092  -e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:19092 -e KAFKA_HEAP_OPTS="-Xmx256M -Xms128M"  wurstmeister/kafka

docker run  -d --name kafka -p 9092:9092  --env KAFKA_ADVERTISED_HOST_NAME=localhost  -e KAFKA_ZOOKEEPER_CONNECT=host.docker.internal:2181 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://host.docker.internal:9092  -e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092 -e KAFKA_HEAP_OPTS="-Xmx256M -Xms128M"  wurstmeister/kafka


docker pull wurstmeister/kafka 
docker run  -d --name kafka-dev -p 9092:9092  --env KAFKA_ADVERTISED_HOST_NAME=localhost  -e KAFKA_ZOOKEEPER_CONNECT=host.docker.internal:2181 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://host.docker.internal:9092  -e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092 -e KAFKA_HEAP_OPTS="-Xmx256M -Xms128M"  wurstmeister/kafka


docker pull sheepkiller/kafka-manager
docker run -it -d --rm  -p 9000:9000 -e ZK_HOSTS="ip:2181"  sheepkiller/kafka-manager


docker run -it -d --rm  -p 9000:9000 -e ZK_HOSTS="host.docker.internal:2181"  sheepkiller/kafka-manager

net stop/start winnat


netsh int ipv4 set dynamic tcp start=49152 num=16384

netsh int ipv4 show excludedportrange protocol=tcp


docker run  -d --name kafka-dev -p 9092:9092  --env KAFKA_ADVERTISED_HOST_NAME=localhost  -e KAFKA_ZOOKEEPER_CONNECT=host.docker.internal:2181 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://host.docker.internal:9092  -e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092 -e KAFKA_HEAP_OPTS="-Xmx256M -Xms128M"  wurstmeister/kafka

