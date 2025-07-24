import os
from typing import Any

import redis


def redis_connection() -> redis.Redis:
    hostname = os.environ.get("REDIS_HOSTNAME", "redis")
    port = int(os.environ.get("REDIS_PORT", "6379"))

    return redis.Redis(host=hostname, port=port)


class Cache:
    """Basic caching interface for `pems_data`."""

    def __init__(self):
        self.r = redis_connection()

    def is_available(self) -> bool:
        """Return a bool indicating if the cache backend is available or not."""
        return self.r.ping() is True

    def get(self, key: str) -> Any:
        """Get a raw value from the cache, or None if the key doesn't exist.

        Args:
            key (str): The item's cache key.
        """
        value = self.r.get(key)
        return value

    def set(self, key: str, value: Any) -> None:
        """Set a value in the cache.

        Args:
            key (str): The item's cache key.
            value (Any): The item's value to store in the cache.
        """
        self.r.set(key, value)
