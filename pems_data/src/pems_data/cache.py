import logging
import os
from typing import Any, Callable

import redis

logger = logging.getLogger(__name__)


def redis_connection() -> redis.Redis:
    hostname = os.environ.get("REDIS_HOSTNAME", "redis")
    port = int(os.environ.get("REDIS_PORT", "6379"))

    logger.debug(f"Connecting to redis @ {hostname}:{port}")
    return redis.Redis(host=hostname, port=port)


class Cache:
    """Basic caching interface for `pems_data`."""

    def __init__(self):
        self.r = redis_connection()

    def is_available(self) -> bool:
        """Return a bool indicating if the cache backend is available or not."""
        available = self.r.ping() is True
        logger.debug(f"cache is available: {available}")
        return available

    def get(self, key: str, mutate_func: Callable[[Any], Any] = None) -> Any:
        """Get a raw value from the cache, or None if the key doesn't exist.

        Args:
            key (str): The item's cache key.
            mutate_func (callable): If provided, call this on the cached value and return its result.
        """
        logger.debug(f"read from cache: {key}")
        value = self.r.get(key)
        if value and mutate_func:
            return mutate_func(value)
        return value

    def set(self, key: str, value: Any, mutate_func: Callable[[Any], Any] = None) -> None:
        """Set a value in the cache.

        Args:
            key (str): The item's cache key.
            value (Any): The item's value to store in the cache.
            mutate_func (callable): If provided, call this on the value and insert the result in the cache.
        """
        if mutate_func:
            value = mutate_func(value)
        logger.debug(f"store in cache: {key}")
        self.r.set(key, value)
