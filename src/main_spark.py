from pyspark.sql import SparkSession

from src.schemas import traffic_sensor_schema
from src.crud import load_to_mongo, mongo
import src.spark_process as sp


# Get or create SparkSession with needed packages for mongo and xml
def get_spark_session() -> SparkSession:
    spark_session = SparkSession \
        .builder \
        .config("spark.jars.packages", "com.databricks:spark-xml_2.12:0.13.0") \
        .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.1.1") \
        .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.1.1") \
        .config("spark.mongodb.read.connection.uri", "mongodb://mongo:27017/myapp.historic") \
        .config("spark.mongodb.write.connection.uri", "mongodb://mongo:27017/myapp.historic") \
        .config("spark.submit.pyFiles", "src/crud.py") \
        .getOrCreate()

    logger = spark_session._jvm.org.apache.log4j
    logger.LogManager.getLogger("org").setLevel(logger.Level.FATAL)
    spark_session.sql("set spark.sql.legacy.timeParserPolicy=LEGACY")
    return spark_session


# Read, preprocess and load data to mongo, and check everything is correct in database
def df_pipeline(spark_session: SparkSession):
    sp.request_data()
    mongo.get_mongo_client()
    df = sp.read_data(spark_session, traffic_sensor_schema)
    df = sp.clean_data(df)
    df = sp.utm_to_latlong(df)
    df = sp.get_districts(df)
    df = sp.assign_colors(df)
    mongo.health_check()
    load_to_mongo(df)
    return df

if __name__ == "__main__":
    spark = get_spark_session()
    df = sp.read_data(spark, traffic_sensor_schema)
    df = sp.clean_data(df)
    df = sp.utm_to_latlong(df)
    df = sp.get_districts(df)
    df = sp.assign_colors(df)
    mongo.health_check()
    df.show()
