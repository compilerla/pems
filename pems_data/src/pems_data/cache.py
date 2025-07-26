import logging
import os
from typing import Any, Callable

import pandas as pd
import redis

from pems_data.serialization import arrow_bytes_to_df, df_to_arrow_bytes

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

    @classmethod
    def build_key(cls, *args) -> str:
        """Build a cache key from the given parts."""
        return ":".join([str(a).lower() for a in args])

    def __init__(self, host: str = None, port: int = None):
        """Create a new instance of the Cache interface.

        Args:
            host (str): (Optional) The hostname of the cache backend.
            port (int): (Optional) The port to connect on the cache backend.
        """

        self.host = host
        self.port = port
        self.c = None

    def _connect(self):
        """Establish a connection to the cache backend if necessary."""
        if not isinstance(self.c, redis.Redis):
            self.c = redis_connection(self.host, self.port)

    def is_available(self) -> bool:
        """Return a bool indicating if the cache backend is available or not."""
        self._connect()
        available = self.c and self.c.ping() is True
        logger.debug(f"cache is available: {available}")
        return available

    def get(self, key: str, mutate_func: Callable[[Any], Any] = None) -> Any:
        """Get a raw value from the cache, or None if the key doesn't exist.

        Args:
            key (str): The item's cache key.
            mutate_func (callable): If provided, call this on the cached value and return its result.
        """
        if self.is_available():
            logger.debug(f"read from cache: {key}")
            value = self.c.get(key)
            if value and mutate_func:
                logger.debug(f"mutating cached value: {key}")
                return mutate_func(value)
            return value
        logger.warning(f"cache unavailable to get: {key}")
        return None

    def get_df(self, key: str) -> pd.DataFrame:
        """Get a `pandas.DataFrame` from the cache, or None if the key doesn't exist."""
        return self.get(key, mutate_func=arrow_bytes_to_df)

    def set(self, key: str, value: Any, mutate_func: Callable[[Any], Any] = None) -> None:
        """Set a value in the cache.

        Args:
            key (str): The item's cache key.
            value (Any): The item's value to store in the cache.
            mutate_func (callable): If provided, call this on the value and insert the result in the cache.
        """
        if self.is_available():
            if mutate_func:
                logger.debug(f"mutating value for cache: {key}")
                value = mutate_func(value)
            logger.debug(f"store in cache: {key}")
            self.c.set(key, value)
        else:
            logger.warning(f"cache unavailable to set: {key}")

    def set_df(self, key: str, value: pd.DataFrame) -> None:
        """Set a `pandas.DataFrame` in the cache."""
        self.set(key, value, mutate_func=df_to_arrow_bytes)
