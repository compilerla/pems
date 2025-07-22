import json
import os

from pems_web.settings import set_aws_db_credentials


def test_runtime_environment_default(settings):
    assert settings.RUNTIME_ENVIRONMENT() == "local"


def test_runtime_environment__local(settings):
    settings.ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
    assert settings.RUNTIME_ENVIRONMENT() == "local"


def test_runtime_environment_dev(settings):
    settings.ALLOWED_HOSTS = ["*"]
    assert settings.RUNTIME_ENVIRONMENT() == "dev"


def test_set_aws_db_credentials(monkeypatch):
    creds = {
        "host": "db.example.com",
        "port": 5432,
        "dbname": "mydb",
        "username": "user",
        "password": "pass",
    }
    monkeypatch.setenv("POSTGRES_SECRET", json.dumps(creds))
    set_aws_db_credentials()

    assert os.environ["POSTGRES_HOSTNAME"] == "db.example.com"
    assert os.environ["POSTGRES_PORT"] == "5432"
    assert os.environ["POSTGRES_DB"] == "mydb"
    assert os.environ["POSTGRES_USER"] == "user"
    assert os.environ["POSTGRES_PASSWORD"] == "pass"


def test_set_aws_db_credentials_missing_keys(monkeypatch):
    # For this test, delete environment variables if they exist
    monkeypatch.delenv("POSTGRES_HOSTNAME", raising=False)
    monkeypatch.delenv("POSTGRES_PORT", raising=False)
    monkeypatch.delenv("POSTGRES_DB", raising=False)
    monkeypatch.delenv("POSTGRES_USER", raising=False)
    monkeypatch.delenv("POSTGRES_PASSWORD", raising=False)

    creds = {
        "host": "db.example.com",
        "port": 5432,
    }
    monkeypatch.setenv("POSTGRES_SECRET", json.dumps(creds))

    set_aws_db_credentials()

    assert os.environ.get("POSTGRES_HOSTNAME") is None
    assert os.environ.get("POSTGRES_PORT") is None
    assert os.environ.get("POSTGRES_DB") is None
    assert os.environ.get("POSTGRES_USER") is None
    assert os.environ.get("POSTGRES_PASSWORD") is None
