import json
from typing import Any

import redis.asyncio as redis

from src.util.cache.cache import Cache


class RedisCache(Cache):
    def __init__(
            self,
            host: str,
            port: int,
            decode_responses: bool
    ):
        self.connection = redis.Redis(host=host, port=port, decode_responses=decode_responses)

    async def get(self, key: str) -> Any:
        return await self.connection.get(key)

    async def set(self, key: str, value: Any, ttl: int = None):
        await self.connection.set(key, value, ex=ttl)

    async def delete(self, key: str) -> None:
        await self.connection.delete(key)
