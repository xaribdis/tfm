from pyspark.sql import SparkSession
from schemas import traffic_sensor_schema
from preprocess_data import read_data, df_to_json
from rdb import json_to_redis, get_redis

custom_schema = traffic_sensor_schema


def get_spark_session() -> SparkSession:
    spark_session = SparkSession \
        .builder \
        .config("spark.jars.packages", "com.databricks:spark-xml_2.12:0.13.0") \
        .getOrCreate()

    logger = spark_session._jvm.org.apache.log4j
    logger.LogManager.getLogger("org").setLevel(logger.Level.FATAL)
    return spark_session


if __name__ == "__main__":
    spark_session = get_spark_session()
    # TODO load last 24 hours data from mongo
    while True:
        # TODO filter out oldest entries
        df = read_data(spark_session, custom_schema)
        # TODO union with last 24 hours df



