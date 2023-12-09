FROM bitnami/spark:3.3.3

# Add necessary jars for mongo and to parse xml
COPY /spark/jars/mongo-spark-connector_2.12-10.1.1.jar jars/mongo-spark-connector_2.12-10.1.1.jar
COPY /spark/jars/spark-xml_2.12-0.13.0.jar jars/spark-xml_2.12-0.13.0.jar
COPY /spark/jars/bson-4.10.2.jar jars/bson-4.10.2.jar
COPY /spark/jars/mongodb-driver-sync-4.10.2.jar jars/mongodb-driver-sync-4.10.2.jar
COPY /spark/jars/mongodb-driver-core-4.10.2.jar jars/mongodb-driver-core-4.10.2.jar
COPY ./init.sh /init.sh

USER root

RUN  chmod +x /init.sh

ADD app ./code/app

RUN mkdir ./code/data

COPY requirements.txt ./code
COPY /data/madrid-districts.geojson ./code/data/madrid-districts.geojson

WORKDIR /opt/bitnami/spark/code/

RUN pip install --no-cache-dir --use-pep517 --upgrade --user -r requirements.txt
