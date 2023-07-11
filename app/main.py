from pyspark.sql import SparkSession
from schemas import traffic_sensor_schema
from preprocess_data import read_data, utm_to_latlong, request_data
from crud import load_to_mongo

custom_schema = traffic_sensor_schema


def get_spark_session() -> SparkSession:
    spark_session = SparkSession \
        .builder \
        .config("spark.jars.packages", "com.databricks:spark-xml_2.12:0.13.0") \
        .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.1.1") \
        .config("spark.mongodb.read.connection.uri", "mongodb://127.0.0.1/myapp.story") \
        .config("spark.mongodb.write.connection.uri", "mongodb://127.0.0.1/myapp.story") \
        .getOrCreate()

    logger = spark_session._jvm.org.apache.log4j
    logger.LogManager.getLogger("org").setLevel(logger.Level.FATAL)
    return spark_session


def df_pipeline():
    request_data()
    spark_session = get_spark_session()
    df = read_data(spark_session, custom_schema)
    return df.toPandas()
    # load_to_mongo(df)
