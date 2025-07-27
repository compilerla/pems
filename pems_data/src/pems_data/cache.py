"""The primary caching interface for `pems_data`."""

import logging
import os
from typing import Any, Callable

import pandas as pd
import redis

from pems_data.serialization import arrow_bytes_to_df, df_to_arrow_bytes

logger = logging.getLogger(__name__)


def redis_connection(host: str = None, port: int = None, **kwargs: dict[str, Any]) -> redis.Redis | None:
    """Try to create a new connection to a redis backend. Return None if the connection fails.

    Uses the `REDIS_HOSTNAME` and `REDIS_PORT` environment variables as fallback.

    Args:
        host (str): (Optional) The redis hostname
        port (int): (Optional) The port to connect on

    Returns:
        value (redis.Redis): A Redis instance connected to `host:port`, or None if the connection failed.
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
    """Basic wrapper for a cache backend."""

    @classmethod
    def build_key(cls, *args: Any) -> str:
        """Build a standard cache key from the given parts.

        Args:
            *args (tuple[Any]): The individual parts that make up the key

        Returns:
            value (str): A standard representation of the parts for use in a cache key.
        """
        return ":".join([str(a).lower() for a in args])

    def __init__(self, host: str = None, port: int = None):
        """Create a new instance of the Cache interface.

        Args:
            host (str): (Optional) The hostname of the cache backend
            port (int): (Optional) The port to connect on the cache backend
        """

        self.host = host
        self.port = port
        self.c = None

    def _connect(self) -> None:
        """Establish a connection to the cache backend if necessary."""
        if not isinstance(self.c, redis.Redis):
            self.c = redis_connection(self.host, self.port)

    def is_available(self) -> bool:
        """Return a bool indicating if the cache backend is available or not.

        Returns:
            value (bool): True if the connection and backend is available; False otherwise
        """
        self._connect()
        available = self.c and self.c.ping() is True
        logger.debug(f"cache is available: {available}")
        return available

    def get(self, key: str, mutate_func: Callable[[Any], Any] = None) -> Any | None:
        """Get a raw value from the cache, or None if the key doesn't exist.

        Args:
            key (str): The item's cache key
            mutate_func (callable): (Optional) If provided, call this on the cached value and return its result

        Returns:
            value (Any | None): The value from the cache, optionally mutated by mutate_func, or None.
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
        """Get a DataFrame from the cache, or an empty DataFrame if the key wasn't found.

        Args:
            key (str): The item's cache key

        Returns:
            value (pandas.DataFrame): The DataFrame materialized from the cache, or an empty DataFrame if the key wasn't found.
        """
        return self.get(key, mutate_func=arrow_bytes_to_df)

    def set(self, key: str, value: Any, ttl: int = None, mutate_func: Callable[[Any], Any] = None) -> None:
        """Set a value in the cache, with an optional TTL (seconds until expiration).

        Args:
            key (str): The item's cache key
            value (Any): The item's value to store in the cache
            ttl (int): (Optional) Seconds until expiration
            mutate_func (callable): (Optional) If provided, call this on the value and insert the result in the cache
        """
        if self.is_available():
            if mutate_func:
                logger.debug(f"mutating value for cache: {key}")
                value = mutate_func(value)
            logger.debug(f"store in cache: {key}")
            self.c.set(key, value, ex=ttl)
        else:
            logger.warning(f"cache unavailable to set: {key}")

    def set_df(self, key: str, value: pd.DataFrame, ttl: int = None) -> None:
        """Set a DataFrame in the cache, with an optional TTL (seconds until expiration).

        Args:
            key (str): The item's cache key
            value (Any): The DataFrame to store in the cache
            ttl (int): (Optional) Seconds until expiration
        """
        self.set(key, value, ttl=ttl, mutate_func=df_to_arrow_bytes)
