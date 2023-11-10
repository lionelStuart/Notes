import logging
import sys

import json
from pyflink.common import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import FlinkKafkaProducer, FlinkKafkaConsumer, KafkaSink
from pyflink.datastream.formats.csv import CsvRowSerializationSchema, CsvRowDeserializationSchema
from pyflink.datastream.formats.json import JsonRowSerializationSchema, JsonRowDeserializationSchema
from pyflink.common.serialization import SimpleStringSchema
from pyflink.table import Row

glb_env = {
    'kafka_addr':'host.docker.internal:9092',
    # 'kafka_addr':'10.107.89.129:9092',
    'kafka_input_topic': 'gogo-visit',
    'kafka_output_topic':'gogo-agg-visit',
}

def write_to_kafka(env: StreamExecutionEnvironment):
    # 用Json String序列化
    # serialization_schema = JsonRowSerializationSchema.Builder() \
    #     .with_type_info(row_type_info) \
    #     .build()
    # kafka_producer = FlinkKafkaProducer(
    #     topic=glb_env['kafka_output_topic'],
    #     serialization_schema=SimpleStringSchema(),
    #     producer_config={'bootstrap.servers': glb_env['kafka_addr']},
    #     kafka_producer_pool_size=1 )

    # ds = env.from_collection(
    #     [(1, 'hi'), (2, 'hello'), (3, 'hi'), (4, 'hello'), (5, 'hi'), (6, 'hello'), (6, 'hello')],
    #     type_info=type_info)
    # 用指定Schema序列化
    row_type_info = Types.ROW_NAMED(['account', 'count'],[Types.STRING(), Types.INT()])
    serialization_schema = JsonRowSerializationSchema.Builder() \
        .with_type_info(row_type_info) \
        .build()
    kafka_producer = FlinkKafkaProducer(
        topic=glb_env['kafka_output_topic'],
        serialization_schema=serialization_schema,
        producer_config={'bootstrap.servers': glb_env['kafka_addr']},
        kafka_producer_pool_size=1 )


    return kafka_producer

def read_from_kafka(env: StreamExecutionEnvironment):
    row_type_info = Types.ROW_NAMED(['Id', 'Account', 'Time'],[Types.INT(), Types.STRING(), Types.STRING()])
    deserialization_schema = JsonRowDeserializationSchema.Builder() \
        .type_info(row_type_info) \
        .build()
    # deserialization_schema = CsvRowDeserializationSchema.Builder(type_info).build()

    kafka_consumer = FlinkKafkaConsumer(
        topics=glb_env['kafka_input_topic'],
        deserialization_schema=deserialization_schema,
        properties={'bootstrap.servers': glb_env['kafka_addr'], 'group.id': 'test_group_1'}
    )

    ds = env.add_source(kafka_consumer)
    return ds


def tuple_to_row(t):
    # 提前json序列化
    v = {
        'account':t[0],
        'count':t[1],
    }
    return str(json.dumps(v))
    return v

def tuple_to_row2(t):
    # 返回row
    v = Row(account=t[0], count=t[1])
    return v


def processing(env):
    ds = read_from_kafka(env)
    
    # 用Json String序列化
    # ds = ds.map(lambda i:(i['Account'], 1), output_type=Types.TUPLE([Types.STRING(), Types.INT()]))\
    #     .key_by(lambda i:i[0])\
    #     .reduce(lambda a, b: (a[0], a[1]+b[1])).map(tuple_to_row, output_type=Types.STRING())

    # 用Scema序列化
    ds = ds.map(lambda i:(i['Account'], 1), output_type=Types.TUPLE([Types.STRING(), Types.INT()]))\
        .key_by(lambda i:i[0])\
        .reduce(lambda a, b: (a[0], a[1]+b[1])).map(tuple_to_row2, output_type=Types.ROW_NAMED(['account', 'count'],[Types.STRING(), Types.INT()]))
    
    # reduce的结果为tuple, Kafka输入为Row,tuple不能转Row，reduce后必须有一次map
    out_prod = write_to_kafka(env)
    ds.add_sink(out_prod)
    env.execute()

if __name__ == '__main__':
    env = StreamExecutionEnvironment.get_execution_environment()
    env.add_jars("file:///home/phoenix/wsl/project/note/Notes/kube/flink/task/src/flink-sql-connector-kafka-3.0.1-1.18.jar")
    env.add_jars("file:///home/phoenix/wsl/project/note/Notes/kube/flink/task/src/flink-connector-kafka-3.0.1-1.18.jar")

    
    print("start writing data to kafka")

    processing(env)
