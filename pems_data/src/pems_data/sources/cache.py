import pandas as pd

from pems_data.cache import Cache
from pems_data.sources import IDataSource


class CachingDataSource(IDataSource):
    """
    A DataSource decorator that adds a caching layer to another data source.
    """

    def __init__(self, data_source: IDataSource, cache: Cache):
        self.cache = cache
        self.data_source = data_source

    def read(self, identifier: str, **kwargs) -> pd.DataFrame:
        # use cache key from the arguments, fallback to identifier
        cache_key = kwargs.get("cache_key", identifier)

        # try to get df from cache
        cached_df = self.cache.get_df(cache_key)
        if cached_df is not None:
            return cached_df

        # on miss, call the wrapped source
        df = self.data_source.read(identifier, **kwargs)
        # store the result in the cache
        self.cache.set_df(cache_key, df)

        return df
