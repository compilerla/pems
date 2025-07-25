import redis
import pytest

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
    @pytest.fixture
    def mock_redis_connection(self, mocker):
        mock_redis = mocker.patch("pems_data.cache.redis_connection")
        mock_redis.return_value = mocker.Mock(spec=redis.Redis)
        return mock_redis.return_value

    @pytest.fixture
    def cache(self, mock_redis_connection):
        return Cache()

    def test_init_creates_redis_connection(self, mock_redis_connection):
        cache = Cache()
        assert cache.r == mock_redis_connection

    def test_is_available_true(self, cache: Cache, mock_redis_connection):
        mock_redis_connection.ping.return_value = True

        assert cache.is_available() is True
        mock_redis_connection.ping.assert_called_once()

    def test_is_available_false(self, cache: Cache, mock_redis_connection):
        mock_redis_connection.ping.return_value = False

        assert cache.is_available() is False
        mock_redis_connection.ping.assert_called_once()

    def test_get(self, cache: Cache, mock_redis_connection):
        expected = b"test-value"
        mock_redis_connection.get.return_value = expected

        result = cache.get("test-key")

        assert result == expected
        mock_redis_connection.get.assert_called_once_with("test-key")

    def test_get_mutate(self, cache: Cache, mock_redis_connection):
        expected = 2
        mock_redis_connection.get.return_value = 1

        result = cache.get("test-key", lambda v: v + 1)

        assert result == expected
        mock_redis_connection.get.assert_called_once_with("test-key")

    def test_set(self, cache: Cache, mock_redis_connection):
        cache.set("test-key", "test-value")

        mock_redis_connection.set.assert_called_once_with("test-key", "test-value")

    def test_set_mutate(self, cache: Cache, mock_redis_connection):
        expected = 2

        cache.set("test-key", 1, lambda v: v + 1)

        mock_redis_connection.set.assert_called_once_with("test-key", expected)
