#!/bin/bash
bin/spark-class org.apache.spark.deploy.master.Master
python ./src/app.py