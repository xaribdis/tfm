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
    StructField("subarea", IntegerType(), True),
    StructField("st_x", DoubleType(), True),
    StructField("st_y", DoubleType(), True)
])

story_data_schema = StructType([
    StructField("idelem", IntegerType(), False),
    StructField("carga", IntegerType(), True),
    StructField("distrito", StringType(), True),
    StructField("fecha_hora", TimestampType, True)
])

