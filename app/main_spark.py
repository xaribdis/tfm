from pyspark.sql import SparkSession
from schemas import traffic_sensor_schema, historic_data_schema
from spark_process import read_data, utm_to_latlong, request_data, get_districts, \
    cast_to_datetime
from crud import load_to_mongo, mongo
from spark_process import field_larger_than, agg_districts, \
    agg_subzones_of_district_by_time, agg_subzones_of_district
from pyspark.sql.types import StringType
from spark_process import get_historic_data_df, filter_district


# Get or create SparkSession with needed packages for mongo and xml
def get_spark_session() -> SparkSession:
    # TODO load from config
    spark_session = SparkSession \
        .builder \
        .config("spark.jars.packages", "com.databricks:spark-xml_2.12:0.13.0") \
        .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.1.1") \
        .config("spark.mongodb.read.connection.uri", "mongodb://127.0.0.1/myapp.historic") \
        .config("spark.mongodb.write.connection.uri", "mongodb://127.0.0.1/myapp.historic") \
        .config("spark.submit.pyFiles", "app/crud.py") \
        .getOrCreate()

    logger = spark_session._jvm.org.apache.log4j
    logger.LogManager.getLogger("org").setLevel(logger.Level.FATAL)
    return spark_session


# Read, preprocess and load data to mongo, and check everything is correct in database
def df_pipeline(spark_session: SparkSession):
    request_data()
    # spark_session = get_spark_session()
    mongo.get_mongo_client()
    df = read_data(spark_session, traffic_sensor_schema)
    df = utm_to_latlong(df)
    df = get_districts(df)
    mongo.healthz()
    load_to_mongo(df)
    return df


if __name__ == "__main__":
    spark_session = get_spark_session()
    df = df_pipeline(spark_session)
    filtered_df = filter_district(df, 'Arganzuela')
    filtered_df.show()
    # print(filtered_df)

    # df.groupBy('distrito', 'subarea').count().groupby('distrito').count().show()
    # df = get_historic_data_df(spark_session, historic_data_schema)
    # filtered_df = agg_subzones_of_district_by_time(df, 'Arganzuela')
    # filtered_df = cast_to_datetime(filtered_df)
    # print(filtered_df.pivot(index='fecha_hora', columns='subarea', values='avg(carga)'))
