# Import SparkSession
from pyspark.sql import SparkSession


def createSession() -> SparkSession:
    spark = SparkSession.builder \
        .master("local[*]") \
        .appName("IUM") \
        .config("spark.sql.warehouse.dir", "./spark-warehouse") \
        .enableHiveSupport() \
        .getOrCreate()

    spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
    spark.conf.set(
        "spark.sql.execution.arrow.pyspark.fallback.enabled", "true"
    )
    spark.sparkContext.setLogLevel("ERROR")
    return spark
