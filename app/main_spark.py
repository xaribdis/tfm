from pyspark.sql import SparkSession
from schemas import traffic_sensor_schema, historic_data_schema
from crud import load_to_mongo, mongo
from pyspark.sql.types import StringType
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
    df = sp.utm_to_latlong(df)
    df = sp.get_districts(df)
    df = sp.assign_colors(df)
    mongo.healthz()
    load_to_mongo(df)
    return df


# if __name__ == "__main__":
#     spark_session = get_spark_session()
#     df = df_pipeline(spark_session)
#     filtered_df = sp.filter_district(df, 'Arganzuela')
#     filtered_df = sp.get_n_first_elements_by_field(filtered_df, 10, 'intensidad')
#     filtered_df.show()
#     print(constants.subarea_colors['Arganzuela'])
#     filtered_df['subarea_colors'] = constants.subarea_colors['Arganzuela']
#     print(filtered_df)


#     with open('colorfile.txt', 'w') as file:
#         for district in constants.districts.keys():
#             print(district)
#             file.write(f"{district}: {sp.generate_subarea_colors(df, district)} \n")
# #
#
