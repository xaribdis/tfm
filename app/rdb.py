from typing import Optional
import redis
import structlog
from redis.client import Redis

log = structlog.get_logger("streaming-traffic-data-app.redis")


class RedisClient:
    client: Optional[Redis] = None


# Create a singleton instance of RedisClient. This will be used to store Redis client connection across requests.
_rdb = RedisClient()


def connect_to_redis() -> Redis:
    # Connect to Redis
    # TODO: settings.py
    log.info("Connecting to Redis...")
    return redis.Redis(
        host="0.0.0.0",
        port=6379,
        password=None,
        db=0,
        decode_responses=True
    )


def get_redis() -> Redis:
    # Get or create connection to Redis
    if _rdb.client is None:
        _rdb.client = connect_to_redis()
    return _rdb.client


def load_to_redis(df):
    df.write\
        .format("org.apache.spark.sql.redis")\
        .option("table", "last24hour")\
        .save()
