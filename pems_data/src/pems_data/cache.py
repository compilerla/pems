import logging
import os
from typing import Any, Callable

import redis

logger = logging.getLogger(__name__)


def redis_connection(host: str = None, port: int = None, **kwargs) -> redis.Redis | None:
    """Try to create a new connection to a redis backend. Return None if the connection fails.

    Uses the `REDIS_HOSTNAME` and `REDIS_PORT` environment variables as fallback.

    Args:
        host (str): The redis hostname
        port (int): The port to connect on
    """

    host = host or os.environ.get("REDIS_HOSTNAME", "redis")
    port = int(port or os.environ.get("REDIS_PORT", "6379"))

    logger.debug(f"connecting to redis @ {host}:{port}")

    kwargs["host"] = host
    kwargs["port"] = port

    try:
        return redis.Redis(**kwargs)
    except redis.ConnectionError as ce:
        logger.error(f"connection failed for redis @ {host}:{port}", exc_info=ce)
        return None


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
