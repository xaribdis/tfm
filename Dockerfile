FROM bitnami/spark:3.3.3

COPY /spark/jars/mongo-spark-connector_2.12-10.1.1.jar jars/mongo-spark-connector_2.12-10.1.1.jar
COPY /spark/jars/spark-xml_2.12-0.13.0.jar jars/spark-xml_2.12-0.13.0.jar

# WORKDIR /opt/bitnami/spark/code 

ADD app ./code/app

COPY requirements.txt ./code

USER root

RUN pip install --no-cache-dir --use-pep517 --upgrade --user -r code/requirements.txt
