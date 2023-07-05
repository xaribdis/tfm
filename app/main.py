from pyspark.sql import SparkSession
from schemas import traffic_sensor_schema
from preprocess_data import read_data
from rdb import load_to_redis

custom_schema = traffic_sensor_schema


def get_spark_session() -> SparkSession:
    spark_session = SparkSession \
        .builder \
        .config("spark.jars.packages", "com.databricks:spark-xml_2.12:0.13.0") \
        .config("spark.jars.packages", "com.redislabs:spark-redis:2.3.0") \
        .config("spark.redis.host", "localhost") \
        .config("spark.redis.port", "6379") \
        .getOrCreate()

    logger = spark_session._jvm.org.apache.log4j
    logger.LogManager.getLogger("org").setLevel(logger.Level.FATAL)
    return spark_session


if __name__ == "__main__":
    spark_session = get_spark_session()
    df = read_data(spark_session, custom_schema)
    df.show()

    load_to_redis(df)
    df_2 = spark_session.read.format("redis").option("table", "last24hour").load()
    df_2.show()
