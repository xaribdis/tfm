# FROM apache/spark-py:v3.3.2
FROM python:3.12-alpine

WORKDIR /code

RUN mkdir -p ./data

# COPY /spark/jars /spark/jars

COPY /requirements.txt .

USER root

# RUN groupadd -r apache -g 433 && \
#     useradd -u 431 -r -g apache -s /sbin/nologin -c "Docker image user" apache

RUN pip install --no-cache-dir --upgrade --user -r requirements.txt

COPY ./data/madrid-districts.geojson ./data/madrid-districts.geojson

COPY ./app ./app

EXPOSE 8050

# USER apache
RUN pwd

CMD ["python", "app/app.py"]
