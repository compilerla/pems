from typing import Any
import pandas as pd

from pems_data.cache import Cache
from pems_data.sources import IDataSource


class CachingDataSource(IDataSource):
    """A data source decorator that adds a caching layer to another data source."""

    @property
    def cache(self) -> Cache:
        """
        Returns:
            value (pems_data.cache.Cache): This data source's underlying Cache instance.
        """
        return self._cache

    @property
    def data_source(self) -> IDataSource:
        """
        Returns:
            value (pems_data.sources.IDataSource): This data source's underlying data source instance.
        """
        return self._data_source

    def __init__(self, data_source: IDataSource, cache: Cache):
        """Initialize a new CachingDataSource.

        Args:
            data_source (pems_data.sources.IDataSource): The underlying data source to use for cache misses
            cache (pems_data.cache.Cache): The underlying cache to use for get/set operations
        """
        self._cache = cache
        self._data_source = data_source

    def read(self, identifier: str, cache_opts: dict[str, Any] = {}, **kwargs: dict[str, Any]) -> pd.DataFrame:
        """
        Reads data identified by a generic identifier from the source. Tries the cache first, setting on a miss.

        Args:
            identifier (str): The unique identifier for the data, e.g., an S3 key, a database table name, etc.
            cache_opts (dict[str, Any]): A dictionary of options for configuring caching of the data
            **kwargs (dict[str, Any]): Additional arguments for the underlying read operation, such as 'columns' or 'filters'

        Returns:
            value (pandas.DataFrame): A DataFrame of data read from the cache (or the source), for the given identifier.
        """
        # use cache key from options, fallback to identifier
        cache_key = cache_opts.get("key", identifier)
        ttl = cache_opts.get("ttl")

        # try to get df from cache
        cached_df = self._cache.get_df(cache_key)
        if cached_df is not None:
            return cached_df

        # on miss, call the wrapped source
        df = self._data_source.read(identifier, **kwargs)
        # store the result in the cache
        self._cache.set_df(cache_key, df, ttl=ttl)

        return df
