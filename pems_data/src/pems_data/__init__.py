from pems_data.cache import Cache
from pems_data.services.stations import StationsService
from pems_data.sources.cache import CachingDataSource
from pems_data.sources.s3 import S3DataSource


class ServiceFactory:
    """
    A factory class to create and configure various services.

    Shared dependencies are created once during initialization.
    """

    @property
    def cache(self) -> Cache:
        """
        Returns:
            value (pems_data.cache.Cache): The shared Cache instance managed by this factory.
        """
        return self._cache

    @property
    def s3_source(self) -> S3DataSource:
        """
        Returns:
            value (pems_data.sources.s3.S3DataSource): The shared S3DataSource instance managed by this factory.
        """
        return self._s3_source

    @property
    def caching_s3_source(self) -> CachingDataSource:
        """
        Returns:
            value (pems_data.sources.cache.CachingDataSource): The shared CachingDataSource instance managed by this factory.
        """
        return self._caching_s3_source

    def __init__(self):
        """Initializes a new ServiceFactory and shared dependencies."""
        self._cache = Cache()
        self._s3_source = S3DataSource()
        self._caching_s3_source = CachingDataSource(data_source=self._s3_source, cache=self._cache)

    def stations_service(self) -> StationsService:
        """Creates a fully-configured StationsService.

        Returns:
            value (pems_data.services.stations.StationsService): A StationsService instance configured by the factory.
        """
        return StationsService(data_source=self._caching_s3_source)
