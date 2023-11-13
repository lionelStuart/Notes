import sys

import argparse
from typing import Iterable

from pyflink.datastream.connectors.file_system import FileSink, OutputFileConfig, RollingPolicy

from pyflink.common import Types, WatermarkStrategy, Time, Encoder
from pyflink.common.watermark_strategy import TimestampAssigner
from pyflink.datastream import StreamExecutionEnvironment, ProcessWindowFunction
from pyflink.datastream.window import TumblingEventTimeWindows, TimeWindow
import datetime

class MyTimestampAssigner(TimestampAssigner):
    def extract_timestamp(self, value, record_timestamp) -> int:
        # print('value=', value, 'ret=', int(value[1]))
        tm = datetime.datetime.strptime(value[1], "%Y-%m-%d %H:%M:%S")
        return int(tm.timestamp())
        return int(value[1])


class CountWindowProcessFunction(ProcessWindowFunction[tuple, tuple, str, TimeWindow]):
    def process(self,
                key: str,
                context: ProcessWindowFunction.Context[TimeWindow],
                elements: Iterable[tuple]) -> Iterable[tuple]:
        print([(key, context.window().start, context.window().end, len([e for e in elements]))])
        return [(key, context.window().start, context.window().end, len([e for e in elements]))]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--output',
        dest='output',
        required=False,
        help='Output file to write results to.')

    argv = sys.argv[1:]
    known_args, _ = parser.parse_known_args(argv)
    output_path = known_args.output

    env = StreamExecutionEnvironment.get_execution_environment()
    # write all the data to one file
    env.set_parallelism(1)

    # define the source
    data_stream = env.from_collection([
        ('hi', '2023-11-13 17:41:52'), ('hi', '2023-11-13 17:41:53'), ('hi', '2023-11-13 17:41:54'), ('hi', '2023-11-13 17:41:55'), ('hi', '2023-11-13 17:41:56'), ('hi', '2023-11-13 17:41:56'), ('hi', '2023-11-13 17:41:58'), ('hi', '2023-11-13 17:41:59'),('strong', '2023-11-13 17:41:59'), ('strong', '2023-11-13 17:41:59')],
        type_info=Types.TUPLE([Types.STRING(), Types.STRING()]))

    # define the watermark strategy
    watermark_strategy = WatermarkStrategy.for_monotonous_timestamps() \
        .with_timestamp_assigner(MyTimestampAssigner())

    ds = data_stream.assign_timestamps_and_watermarks(watermark_strategy) \
        .key_by(lambda x: x[0], key_type=Types.STRING()) \
        .window(TumblingEventTimeWindows.of(Time.seconds(5))) \
        .process(CountWindowProcessFunction(),
                 Types.TUPLE([Types.STRING(), Types.INT(), Types.INT(), Types.INT()]))

    # define the sink
    if output_path is not None:
        ds.sink_to(
            sink=FileSink.for_row_format(
                base_path=output_path,
                encoder=Encoder.simple_string_encoder())
            .with_output_file_config(
                OutputFileConfig.builder()
                .with_part_prefix("prefix")
                .with_part_suffix(".ext")
                .build())
            .with_rolling_policy(RollingPolicy.default_rolling_policy())
            .build()
        )
    else:
        print("Printing result to stdout. Use --output to specify output path.")
        ds.print()

    # submit for execution
    env.execute()