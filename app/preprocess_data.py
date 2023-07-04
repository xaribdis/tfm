from pyspark.sql.functions import lit
import requests


# Request the data to the url and save in in an xml file
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


def read_data(spark_session, custom_schema):
    fecha_hora = get_fecha_hora()

    df = spark_session.read \
        .format('xml') \
        .options(rowTag='pm') \
        .load("data/traffic_data.xml", schema=custom_schema)

    df = df.withColumn("fecha_hora", lit(fecha_hora))
    return df
