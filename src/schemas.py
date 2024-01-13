from pyspark.sql.types import IntegerType, StringType, DoubleType, StructField, StructType, TimestampType

traffic_sensor_schema = StructType([
    StructField("idelem", IntegerType(), False),
    StructField("descripcion", StringType(), True),
    StructField("accesoAsociado", IntegerType(), True),
    StructField("intensidad", IntegerType(), True),
    StructField("ocupacion", IntegerType(), True),
    StructField("carga", IntegerType(), True),
    StructField("nivelServicio", IntegerType(), True),
    StructField("intensidadSat", IntegerType(), True),
    StructField("velocidad", IntegerType(), True),
    StructField("error", StringType(), True),
    StructField("subarea", StringType(), True),
    StructField("st_x", StringType(), True),
    StructField("st_y", StringType(), True)
])

historic_data_schema = StructType([
    StructField("idelem", IntegerType(), False),
    StructField("subarea", StringType(), True),
    StructField("carga", IntegerType(), True),
    StructField("distrito", StringType(), True),
    StructField("fecha_hora", TimestampType(), True)
])

