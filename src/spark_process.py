from pyspark.sql.functions import lit, udf, col, to_timestamp, regexp_replace, when
from pyspark.sql.types import DoubleType, StringType
from pyspark.sql import SparkSession, DataFrame
from pyspark import SparkFiles
import requests
import utm
import pandas as pd

from src.crud import query_sensor_districts
from src.config import settings


# Request the data to the url and save in an xml file
def request_data():
    url = "https://datos.madrid.es/egob/catalogo/202087-0-trafico-intensidad.xml"
    header = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36', }
    r = requests.get(url, headers=header)

    with open("data/traffic_data.xml", 'wb') as file:
        file.write(r._content)
    r.close()


# Remove sensors with no data
def clean_data(df):
    df = df.filter(df.carga < 100)
    df = df.filter(df.intensidad > -1)
    df = df.withColumn('subarea', when('velocidad is Not Null'), 'M30').otherwise(col('subarea'))
    return df.withColumn('intensidad', when(col('intensidad') == -1), 0).otherwise(col('intensidad'))


# Get date and hour from xml header
def get_fecha_hora():
    with open("data/traffic_data.xml", encoding="utf-8") as xml:
        xml.readline()
        return xml.readline().split(">", 1)[1].split("<")[0]


# Convert utm coordinates to latitude/longitude
def utm_to_latlong(df: DataFrame) -> DataFrame:
    utm_udf_x = udf(lambda x, y: utm.to_latlon(x, y, 30, 'T')[0].item(), DoubleType())
    utm_udf_y = udf(lambda x, y: utm.to_latlon(x, y, 30, 'T')[1].item(), DoubleType())
    df = df.withColumn("latitud", utm_udf_x(col('st_x'), col('st_y')))
    df = df.withColumn("longitud", utm_udf_y(col('st_x'), col('st_y')))
    df = df.drop("st_x", "st_y")
    return df


def get_districts(df: DataFrame) -> DataFrame:
    districts_udf = udf(lambda x: query_sensor_districts(x))
    df = df.withColumn("distrito", districts_udf(col('idelem')))
    return df


# Read data from xml file into dataframe
def read_data(spark_session: SparkSession, custom_schema) -> DataFrame:
    file_path = SparkFiles.get('traffic_data.xml')
    fecha_hora = get_fecha_hora()
    # print('FECHA_HORA:', fecha_hora)

    df = spark_session.read \
        .format('xml') \
        .options(rowTag='pm') \
        .option("mode", "DROPMALFORMED") \
        .load(file_path, schema=custom_schema)

    df = df.withColumn("fecha_hora", to_timestamp(lit(fecha_hora), "dd/MM/yyyy HH:mm:ss"))
    df = df.withColumn('st_x', regexp_replace('st_x', ',', '.').cast(DoubleType()))
    df = df.withColumn('st_y', regexp_replace('st_y', ',', '.').cast(DoubleType()))
    return df


def get_historic_data_df(spark_session: SparkSession, custom_schema) -> DataFrame:
    """Retrieve historic data from mongo into a dataframe"""
    return spark_session.read.format('mongodb').load(schema=custom_schema)


def agg_districts(df: DataFrame) -> DataFrame:
    return df.groupBy('distrito').avg('intensidad')


def filter_district(df: DataFrame, district: str) -> DataFrame:
    return df.filter(col('distrito') == district)


def agg_subzones_of_district(df: DataFrame, district: str) -> DataFrame:
    return df.groupBy('subarea').avg('carga')


def agg_district_by_time(df: DataFrame) -> DataFrame:
    return df.groupBy('fecha_hora').avg('carga').sort('fecha_hora')


def agg_subzones_of_district_by_time(df: DataFrame) -> DataFrame:
    return df.groupBy('subarea', 'fecha_hora').avg('carga')


# Since Spark 3.3, TimestampType is not compatible with datetime from pandas so I have to do this stupid transformation
def cast_to_datetime(df):
    casted_df = df.withColumn("fecha_hora", df["fecha_hora"].cast(StringType())).toPandas()
    casted_df["fecha_hora"] = pd.to_datetime(casted_df["fecha_hora"], format="%Y-%m-%d %H:%M:%S")
    return casted_df


def field_larger_than(df: DataFrame, field: str, threshold: int) -> DataFrame:
    return df.filter(col(field) > threshold)


def field_less_than(df: DataFrame, field: str, threshold: int) -> DataFrame:
    return df.filter(col(field) < threshold)


def get_subareas_of_district(df: DataFrame, district: str) -> []:
    return filter_district(df, district).select('subarea').distinct().collect()


# Function to generate random colors for each subarea for visualization. Not used in app.
def generate_subarea_colors(df: DataFrame, district) -> dict:
    subareas = get_subareas_of_district(df, district)
    colors = {}
    h = 360 / len(subareas)
    i = 0
    for row in subareas:
        colors[row.subarea] = 'hsl(' + str(i*h) + ',50%' + ',50%)'
        i += 1

    colors['unknown'] = '#39b0b3'
    return colors


def assign_colors(df: DataFrame) -> DataFrame:
    color_udf = udf(lambda x, y: settings.SUBAREA_COLORS[x].get(y, '#39b0b3'))
    return df.withColumn('subarea_color', color_udf(col('distrito'), col('subarea')))


def get_n_first_elements_by_field(df: DataFrame, n: int, field: str) -> DataFrame:
    filtered_df = df.select('idelem', field, 'subarea_color', 'descripcion', 'intensidadSat')
    return filtered_df.withColumn('idelem', filtered_df.idelem.cast(StringType())).sort(field, ascending=False).limit(n).toPandas()
