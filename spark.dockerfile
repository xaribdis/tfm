FROM bitnami/spark:3.3.3

COPY /spark/jars/mongo-spark-connector_2.12-10.1.1.jar jars/mongo-spark-connector_2.12-10.1.1.jar
COPY /spark/jars/spark-xml_2.12-0.13.0.jar jars/spark-xml_2.12-0.13.0.jar
