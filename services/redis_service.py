import redis
from datetime import timedelta

from settings import REDIS_URL

redis = redis.from_url(REDIS_URL)


class RedisService:
    @staticmethod
    def set(key, value, lifetime=300):
        redis.setex(
            key,
            timedelta(seconds=lifetime),
            value=value
        )

    @staticmethod
    def exists(key):
        return redis.exists(key)

    @staticmethod
    def get(key):
        return redis.get(key)

    @staticmethod
    def get_ttl(key):
        return redis.ttl(key)

    @staticmethod
    def flush():
        redis.flushall()
