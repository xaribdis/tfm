from pyspark.sql import SparkSession
from schemas import traffic_sensor_schema       
from pyspark.sql.functions import lit
import time

with open("data/traffic_data.xml", encoding="utf-8") as xml:
    xml.readline()
    fecha_hora = xml.readline().split(">",1)[1].split("<")[0]

spark_session = (SparkSession
                    .builder
                    .config("spark.jars.packages", "com.databricks:spark-xml_2.12:0.13.0") \
                    .getOrCreate())

logger = spark_session._jvm.org.apache.log4j
logger.LogManager.getLogger("org").setLevel(logger.Level.FATAL)

customSchema = traffic_sensor_schema

df = spark_session.read \
        .format('xml') \
        .options(rowTag='pm') \
        .load("data/traffic_data.xml", schema=customSchema)

df = df.withColumn("fecha_hora", lit(fecha_hora))
df.show()