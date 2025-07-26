from pems_data.cache import Cache
from pems_data.services.stations import StationsService
from pems_data.sources.cache import CachingDataSource
from pems_data.sources.s3 import S3DataSource


class ServiceFactory:
    """
    A factory class to create and configure various services.

    Shared dependencies are created once during initialization.
    """

    def __init__(self):
        self.cache = Cache()
        self.s3_source = S3DataSource()
        self.caching_s3_source = CachingDataSource(data_source=self.s3_source, cache=self.cache)

    def stations_service(self) -> StationsService:
        """Creates a fully-configured `StationsService`."""
        return StationsService(data_source=self.caching_s3_source)
