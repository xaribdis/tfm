from pyspark.sql import SparkSession
from schemas import traffic_sensor_schema       

spark_session = (SparkSession
                    .builder
                    .config("spark.jars.packages", "com.databricks:spark-xml_1.12:0.13.0") \
                    .getOrCreate()
                )

logger = spark_session._jvm.org.apache.log4j
logger.LogManager.getLogger("org").setLevel(logger.Level.WARN)

customSchema = traffic_sensor_schema

df = spark_session.read \
        .format('xml') \
        .options(rowTag='pm') \
        .load("data/traffic_data.xml", schema=customSchema)

df.show()
