#!/bin/bash
bin/spark-class org.apache.spark.deploy.master.Master
python ./app/app.py