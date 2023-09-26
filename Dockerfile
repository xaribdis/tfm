FROM apache/spark-py:v3.3.2

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

USER root

RUN groupadd -r apache -g 433 && \
    useradd -u 431 -r -g apache -s /sbin/nologin -c "Docker image user" apache

RUN pip install --no-cache-dir --upgrade --user -r /code/requirements.txt

RUN mkdir -p /code/data

COPY ./data/madrid-districts.geojson /code/data/madrid-districts.geojson
COPY ./app /code/app

EXPOSE 8050

USER apache

CMD ["python", "/code/app.py"]
