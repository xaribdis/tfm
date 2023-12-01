import numpy as np

from pyspark.sql import SparkSession
from schemas import traffic_sensor_schema, historic_data_schema
from crud import load_to_mongo, mongo
# from pyspark.sql.types import StringType
import spark_process as sp

import constants


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
    sp.request_data()
    # spark_session = get_spark_session()
    mongo.get_mongo_client()
    df = sp.read_data(spark_session, traffic_sensor_schema)
    df = sp.clean_data(df)
    df = sp.utm_to_latlong(df)
    df = sp.get_districts(df)
    df = sp.assign_colors(df)
    mongo.healthz()
    load_to_mongo(df)
    return df


# if __name__ == "__main__":
#     spark_session = get_spark_session()
#     df = sp.get_historic_data_df(spark_session, historic_data_schema)
#     filtered_df = sp.agg_district_by_time(df, 'Arganzuela')
#     filtered_df = sp.cast_to_datetime(filtered_df)
#     print(filtered_df.loc[filtered_df['fecha_hora'] > '2023-11-26'])

    # subareas = sp.get_subareas_of_district(df, 'Arganzuela')
    # print(sorted(subareas, key=lambda x: int(x.subarea)))

    # print(df.dtypes)
    # filtered_df = sp.agg_subzones_of_district_by_time(df, 'Arganzuela')
    # filtered_df = sp.cast_to_datetime(filtered_df)
    # filtered_df = filtered_df.pivot(index='fecha_hora', columns='subarea', values='avg(carga)').drop(columns=np.nan)
    # print(filtered_df)
    # print([constants.subarea_colors['Arganzuela'][col] for col in filtered_df])

    # with open('colorfile.txt', 'w') as file:
    #     for district in constants.districts.keys():
    #         print(district)
    #         file.write(f"{district}: {sp.generate_subarea_colors(df, district)} \n")
# #
#
