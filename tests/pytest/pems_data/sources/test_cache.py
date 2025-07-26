import pandas as pd
import pytest

from pems_data.sources import IDataSource
from pems_data.sources.cache import CachingDataSource


class TestCachingDataSource:
    @pytest.fixture
    def mock_source(self, df):
        """Create a mock underlying data source"""

        class MockSource(IDataSource):
            def read(self, identifier: str, **kwargs) -> pd.DataFrame:
                return df

        return MockSource()

    @pytest.fixture
    def mock_cache(self, mocker):
        """Create and configure mock cache"""
        cache = mocker.Mock()
        cache.is_available.return_value = True
        return cache

    @pytest.fixture
    def data_source(self, mock_source, mock_cache) -> CachingDataSource:
        """Create CachingDataSource with mocked dependencies"""
        return CachingDataSource(mock_source, cache=mock_cache)

    def test_read__cache_hit(self, data_source: CachingDataSource, mock_cache, df):
        """Test reading when data is in cache"""
        mock_cache.get_df.return_value = df

        result = data_source.read("test-id")

        mock_cache.get_df.assert_called_once_with("test-id")
        pd.testing.assert_frame_equal(result, df)

    def test_read__cache_miss(self, data_source: CachingDataSource, mock_cache, df):
        """Test reading when data is not in cache"""
        mock_cache.get_df.return_value = None

        result = data_source.read("test-id")

        mock_cache.get_df.assert_called_once_with("test-id")
        mock_cache.set_df.assert_called_once_with("test-id", df, ttl=None)
        pd.testing.assert_frame_equal(result, df)
