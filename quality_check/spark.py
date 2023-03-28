# Import SparkSession
from pyspark.sql import SparkSession


def createSession() -> SparkSession:
    return SparkSession.builder \
        .master("local[*]") \
        .getOrCreate()
