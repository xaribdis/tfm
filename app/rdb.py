from typing import Optional
import redis
import structlog
from redis.client import Redis

log = structlog.get_logger("streaming-traffic-data-app.redis")


def load_to_redis(df):
    # TODO Check that this works
    # TODO add ttl
    df.write\
        .format("org.apache.spark.sql.redis")\
        .option("table", "last24hour")\
        .option("ttl", 300) \
        .save()
