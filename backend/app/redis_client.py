import redis
from .config import settings

redis_client = redis.Redis.from_url(f'{settings.redis_url}', decode_responses=True)
