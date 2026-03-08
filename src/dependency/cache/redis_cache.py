from src.config import settings
from src.util.cache.cache import Cache
from src.util.cache.redis_cache import RedisCache


def get_redis_cache() -> Cache:
    return RedisCache(
        settings.redis_settings.redis_host,
        settings.redis_settings.redis_port,
        settings.redis_settings.redis_decode_responses,
    )