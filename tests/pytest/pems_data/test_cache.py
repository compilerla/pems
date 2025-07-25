import pandas as pd
import pytest
import redis

from pems_data.cache import Cache, redis_connection


class TestRedisConnection:
    @pytest.fixture(autouse=True)
    def mock_redis(self, mocker):
        return mocker.patch("redis.Redis")

    @pytest.fixture
    def redis_host(self):
        return "redis"

    @pytest.fixture
    def redis_port(self):
        return 6379

    def test_redis_connection_default(self, mock_redis, redis_host, redis_port):
        redis_connection()
        mock_redis.assert_called_once_with(host=redis_host, port=redis_port)

    def test_redis_connection_parameters(self, mock_redis):
        redis_connection("custom-host", 1234)
        mock_redis.assert_called_once_with(host="custom-host", port=1234)

    def test_redis_connection_env_vars(self, mock_redis, monkeypatch):
        monkeypatch.setenv("REDIS_HOSTNAME", "custom-host")
        monkeypatch.setenv("REDIS_PORT", "1234")

        redis_connection()
        mock_redis.assert_called_once_with(host="custom-host", port=1234)

    def test_redis_connection_env_vars_and_parameters(self, mock_redis, monkeypatch):
        monkeypatch.setenv("REDIS_HOSTNAME", "env-host")
        monkeypatch.setenv("REDIS_PORT", "1234")

        redis_connection("param-host", 5678)
        mock_redis.assert_called_once_with(host="param-host", port=5678)

    def test_redis_connection_error(self, mock_redis):
        mock_redis.side_effect = redis.ConnectionError

        result = redis_connection()

        mock_redis.assert_called_once()
        assert result is None

    def test_redis_connection_extras(self, mock_redis, redis_host, redis_port):
        redis_connection(extra1="extra1", extra2="extra2")

        mock_redis.assert_called_once_with(host=redis_host, port=redis_port, extra1="extra1", extra2="extra2")


class TestCache:
    @pytest.fixture(autouse=True)
    def mock_redis_connection(self, mocker):
        mock_redis = mocker.patch("pems_data.cache.redis_connection")
        mock_redis.return_value = mocker.Mock(spec=redis.Redis)
        return mock_redis.return_value

    @pytest.fixture
    def cache(self) -> Cache:
        return Cache()

    @pytest.fixture
    def spy_connect(self, cache, mocker):
        return mocker.spy(cache, "_connect")

    @pytest.fixture(autouse=True)
    def mock_is_available(self, mock_redis_connection):
        mock_redis_connection.ping.return_value = True

    def test_init_does_not_create_redis_connection(self, cache: Cache, spy_connect):
        assert hasattr(cache, "c")
        assert cache.c is None
        spy_connect.assert_not_called()

    def test_connect(self, cache: Cache, spy_connect):
        cache._connect()

        spy_connect.assert_called_once()
        assert isinstance(cache.c, redis.Redis)

    def test_is_available_true(self, cache: Cache, mock_redis_connection, spy_connect):
        mock_redis_connection.ping.return_value = True

        assert cache.is_available() is True
        spy_connect.assert_called_once()
        mock_redis_connection.ping.assert_called_once()

    def test_is_available_false(self, cache: Cache, mock_redis_connection, spy_connect):
        mock_redis_connection.ping.return_value = False

        assert cache.is_available() is False
        spy_connect.assert_called_once()
        mock_redis_connection.ping.assert_called_once()

    def test_get(self, cache: Cache, mock_redis_connection, spy_connect):
        expected = b"test-value"
        mock_redis_connection.get.return_value = expected

        result = cache.get("test-key")

        assert result == expected
        spy_connect.assert_called_once()
        mock_redis_connection.get.assert_called_once_with("test-key")

    def test_get__mutate(self, cache: Cache, mock_redis_connection, spy_connect):
        expected = 2
        mock_redis_connection.get.return_value = 1

        result = cache.get("test-key", lambda v: v + 1)

        assert result == expected
        spy_connect.assert_called_once()
        mock_redis_connection.get.assert_called_once_with("test-key")

    def test_set(self, cache: Cache, mock_redis_connection, spy_connect):
        cache.set("test-key", "test-value")

        spy_connect.assert_called_once()
        mock_redis_connection.set.assert_called_once_with("test-key", "test-value")

    def test_set__mutate(self, cache: Cache, mock_redis_connection, spy_connect):
        expected = 2

        cache.set("test-key", 1, lambda v: v + 1)

        spy_connect.assert_called_once()
        mock_redis_connection.set.assert_called_once_with("test-key", expected)

    def test_set__unavailable(self, cache: Cache, mock_redis_connection, spy_connect):
        mock_redis_connection.ping.return_value = False

        cache.set("test-key", "test-value")

        spy_connect.assert_called_once()
        mock_redis_connection.set.assert_not_called()

    def test_get_df(self, cache: Cache, mock_redis_connection, mocker, spy_connect):
        # Mock arrow_bytes_to_df to return a DataFrame
        df = mocker.Mock(spec=pd.DataFrame)
        arrow_bytes = b"arrow-bytes"
        mock_redis_connection.get.return_value = arrow_bytes
        mock_arrow_bytes_to_df = mocker.patch("pems_data.cache.arrow_bytes_to_df", return_value=df)

        result = cache.get_df("df-key")

        spy_connect.assert_called_once()
        mock_redis_connection.get.assert_called_once_with("df-key")
        mock_arrow_bytes_to_df.assert_called_once_with(arrow_bytes)
        assert result == df

    def test_set_df(self, cache: Cache, mock_redis_connection, spy_connect, df):
        """Test setting a DataFrame in the cache"""
        cache.set_df("test-key", df)

        spy_connect.assert_called_once()
        mock_redis_connection.set.assert_called_once()
        # Verify first arg is the key
        assert mock_redis_connection.set.call_args[0][0] == "test-key"
        # Verify second arg is bytes (arrow serialized)
        assert isinstance(mock_redis_connection.set.call_args[0][1], bytes)

    def test_set_df__empty_df(self, cache: Cache, mock_redis_connection, spy_connect):
        empty_df = pd.DataFrame()
        cache.set_df("test-key", empty_df)

        spy_connect.assert_called_once()
        mock_redis_connection.set.assert_called_once()
        # Verify empty DataFrame is handled
        assert isinstance(mock_redis_connection.set.call_args[0][1], bytes)

    def test_set_df__roundtrip(self, cache: Cache, mock_redis_connection, spy_connect, df, mocker):
        # Setup mock to return the serialized value on get
        def mock_set(key, value):
            mock_redis_connection.get.return_value = value

        mock_redis_connection.set.side_effect = mock_set

        # Set the DataFrame
        cache.set_df("test-key", df)

        # Get it back
        result = cache.get_df("test-key")

        pd.testing.assert_frame_equal(result, df)
        spy_connect.assert_has_calls([mocker.call(), mocker.call()])
