from pyspark.sql.functions import lit, udf, col, to_date
from pyspark.sql.types import DoubleType
from pyspark.sql import SparkSession
import requests
import utm


# Request the data to the url and save in an xml file
def request_data():
    url = "https://datos.madrid.es/egob/catalogo/202087-0-trafico-intensidad.xml"
    r = requests.get(url)

    with open("data/traffic_data.xml", 'wb') as file:
        file.write(r._content)
    r.close()


def get_fecha_hora():
    with open("data/traffic_data.xml", encoding="utf-8") as xml:
        xml.readline()
        return xml.readline().split(">", 1)[1].split("<")[0]


def utm_to_latlong(df):
    utm_udf_x = udf(lambda x, y: utm.to_latlon(x, y, 30, 'T')[0].item(), DoubleType())
    utm_udf_y = udf(lambda x, y: utm.to_latlon(x, y, 30, 'T')[1].item(), DoubleType())
    df = df.withColumn("latitud", utm_udf_x(col('st_x'), col('st_y')))
    df = df.withColumn("longitud", utm_udf_y(col('st_x'), col('st_y')))
    df = df.drop("st_x", "st_y")
    return df


def read_data(spark_session: SparkSession, custom_schema):
    fecha_hora = get_fecha_hora()

    df = spark_session.read \
        .format('xml') \
        .options(rowTag='pm') \
        .load("data/traffic_data.xml", schema=custom_schema)

    df = df.withColumn("fecha_hora", to_date(lit(fecha_hora), "dd/MM/yyyy HH:mm:ss"))
    df = utm_to_latlong(df)
    return df

