from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType
from typing import List

# ========= #
#    UDF    #
# ========= #


def total_time_listened_ms(events: List[str], start_s: List[int], duration_ms: int) -> int:
    previous_start = 0
    plays = 0
    skips = 0
    duration_skipped = 0
    for event, start in sorted(zip(events, start_s), key=lambda x: x[1]):
        if event == 'PLAY':
            plays += 1
            previous_start = start
        elif event == 'SKIP':
            skips += 1
            duration_skipped += start - previous_start

    return duration_skipped * 1000 + duration_ms * (plays - skips)


def register_udfs(spark: SparkSession) -> None:
    spark.udf.register(
        "total_time_listened_ms",
        total_time_listened_ms,
        IntegerType()
    )
