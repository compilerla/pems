import pytest

from pems_data import ServiceFactory
from pems_data.cache import Cache
from pems_data.services.stations import StationsService
from pems_data.sources.cache import CachingDataSource
from pems_data.sources.s3 import S3DataSource


class TestServiceFactory:

    @pytest.fixture
    def factory(self):
        return ServiceFactory()

    def test_init_cache(self, factory: ServiceFactory):
        assert isinstance(factory.cache, Cache)

    def test_init_s3_source(self, factory: ServiceFactory):
        assert isinstance(factory.s3_source, S3DataSource)

    def test_init_caching_s3_source(self, factory: ServiceFactory):
        assert isinstance(factory.caching_s3_source, CachingDataSource)
        assert isinstance(factory.caching_s3_source.data_source, S3DataSource)
        assert isinstance(factory.caching_s3_source.cache, Cache)

    def test_stations_service(self, factory: ServiceFactory):
        service = factory.stations_service()

        assert isinstance(service, StationsService)
        assert service.data_source == factory.caching_s3_source
