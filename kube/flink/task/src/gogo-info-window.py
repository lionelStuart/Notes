from ast import Tuple
import logging
import sys

import json
from pyflink.common import Types
from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.datastream.connectors.kafka import FlinkKafkaProducer, FlinkKafkaConsumer, KafkaSink
from pyflink.datastream.formats.csv import CsvRowSerializationSchema, CsvRowDeserializationSchema
from pyflink.datastream.formats.json import JsonRowSerializationSchema, JsonRowDeserializationSchema
from pyflink.common.serialization import SimpleStringSchema
from pyflink.table import Row
from pyflink.datastream import StreamExecutionEnvironment, ProcessWindowFunction
from pyflink.datastream.window import TumblingEventTimeWindows, TimeWindow
from pyflink.common.watermark_strategy import TimestampAssigner
import datetime
from pyflink.common import Types, WatermarkStrategy, Time, Encoder
from typing import Iterable

glb_env = {
    'kafka_addr':'host.docker.internal:9092',
    # 'kafka_addr':'10.107.89.129:9092',
    'kafka_input_topic': 'gogo-visit',
    'kafka_output_topic':'gogo-agg-visit',
}

class MyTimestampAssigner(TimestampAssigner):
    def extract_timestamp(self, value, record_timestamp) -> int:
        tm = datetime.datetime.strptime(value[2], "%Y-%m-%d %H:%M:%S")
        return int(tm.timestamp()*1000)


class CountWindowProcessFunction(ProcessWindowFunction[Row, Tuple, str, TimeWindow]):
    def process(self,
                key: str,
                context: ProcessWindowFunction.Context[TimeWindow],
                elements: Iterable[tuple]) -> Iterable[tuple]:
        return [(key, context.window().start, context.window().end, len([e for e in elements]))]


def write_to_kafka(env: StreamExecutionEnvironment):
    # 用Json String序列化
    kafka_producer = FlinkKafkaProducer(
        topic=glb_env['kafka_output_topic'],
        serialization_schema=SimpleStringSchema(),
        producer_config={'bootstrap.servers': glb_env['kafka_addr']},
        kafka_producer_pool_size=2)
    return kafka_producer

def read_from_kafka(env: StreamExecutionEnvironment):
    row_type_info = Types.ROW_NAMED(['Id', 'Account', 'Time'],[Types.INT(), Types.STRING(), Types.STRING()])
    deserialization_schema = JsonRowDeserializationSchema.Builder() \
        .type_info(row_type_info) \
        .build()

    kafka_consumer = FlinkKafkaConsumer(
        topics=glb_env['kafka_input_topic'],
        deserialization_schema=deserialization_schema,
        properties={'bootstrap.servers': glb_env['kafka_addr'], 'group.id': 'test_group_1', 'auto.offset.reset': 'latest'}
    )

    ds = env.add_source(kafka_consumer)
    return ds

def read_from_sample(env: StreamExecutionEnvironment):
    data_stream = env.from_collection([
        (0,'hi', '2023-11-13 17:41:52'), 
        (1,'hi', '2023-11-13 17:41:53'), 
        (2,'hi', '2023-11-13 17:41:54'), 
        (3,'hi', '2023-11-13 17:41:55'), 
        (4,'hi', '2023-11-13 17:41:56'), 
        (5,'hi', '2023-11-13 17:41:56'), 
        (6,'hi', '2023-11-13 17:41:58'), 
        (7,'hi', '2023-11-13 17:41:59'),
        (8,'strong', '2023-11-13 17:41:59'), 
        (9,'strong', '2023-11-13 17:41:59')],
        type_info=Types.ROW([Types.INT(),Types.STRING(), Types.STRING()]))
    
    return data_stream

def tuple_to_row(t):
    # 提前json序列化
    v = {
        'account':t[0],
        'start':t[1],
        'end':t[2],
        'count':t[3],
 
    }
    return str(json.dumps(v))
    return v

def tuple_to_row2(t):
    # 返回row
    v = Row(account=t[0], count=t[1])
    return v


def processing(env):
    ds = read_from_kafka(env)
    # ds = read_from_sample(env)
    
    watermark_strategy = WatermarkStrategy.for_monotonous_timestamps() \
    .with_timestamp_assigner(MyTimestampAssigner())

    ds = ds.assign_timestamps_and_watermarks(watermark_strategy)\
        .key_by(lambda i:i[1], key_type = Types.STRING())\
        .window(TumblingEventTimeWindows.of(Time.seconds(5)))\
        .process(CountWindowProcessFunction(), 
               Types.TUPLE([Types.STRING(), Types.INT(), Types.INT(), Types.INT()]))\
        .map(tuple_to_row, output_type=Types.STRING())
    # ds.print()

    out_prod = write_to_kafka(env)
    ds.add_sink(out_prod)
    env.execute()

if __name__ == '__main__':
    env = StreamExecutionEnvironment.get_execution_environment()
    env.add_jars("file:///home/phoenix/wsl/project/note/Notes/kube/flink/task/src/flink-sql-connector-kafka-3.0.1-1.18.jar")
    env.add_jars("file:///home/phoenix/wsl/project/note/Notes/kube/flink/task/src/flink-connector-kafka-3.0.1-1.18.jar")

    env.set_parallelism(1)
    env.set_stream_time_characteristic(TimeCharacteristic.EventTime)
    
    print("start writing data to kafka")

    processing(env)
