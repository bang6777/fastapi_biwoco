import redis
from core.config import config


class RedisClient:
    def __init__(self):
        self.redis = redis.StrictRedis(
            host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB, decode_responses=True
        )

    def set(self, key: str, value: str, expire: int = 3600):
        self.redis.setex(key, expire, value)

    def get_value(self, key: str) -> str:
        value = self.redis.get(key)
        return value

    def delete(self, key: str):
        self.redis.delete(key)
