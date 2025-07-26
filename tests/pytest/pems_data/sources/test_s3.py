import re

import pytest

from pems_data.sources.s3 import S3DataSource


class TestS3DataSource:

    @pytest.fixture
    def data_source(self) -> S3DataSource:
        return S3DataSource()

    @pytest.fixture(autouse=True)
    def mock_s3(self, mocker):
        s3 = mocker.patch("boto3.client").return_value
        s3.list_objects.return_value = {
            "Contents": [
                {"Key": "path1/file2.json"},
                {"Key": "path2/file1.json"},
                {"Key": "path1/file1.json"},
            ]
        }
        return s3

    @pytest.fixture(autouse=True)
    def mock_read_parquet(self, mocker):
        return mocker.patch("pandas.read_parquet")

    def test_name_custom(self):
        assert S3DataSource("name").name == "name"

    def test_name_default(self):
        assert S3DataSource().name == S3DataSource.default_bucket

    def test_get_prefixes__default(self, data_source: S3DataSource, mock_s3):
        result = data_source.get_prefixes()

        mock_s3.list_objects.assert_called_once_with(Bucket=data_source.name, Prefix="")
        assert result == ["path1/file1.json", "path1/file2.json", "path2/file1.json"]

    def test_get_prefixes__filter_pattern(self, data_source: S3DataSource):
        result = data_source.get_prefixes(re.compile("path1/.+"))

        assert result == ["path1/file1.json", "path1/file2.json"]

    def test_get_prefixes__initial_prefix(self, data_source: S3DataSource, mock_s3):
        data_source.get_prefixes(initial_prefix="prefix")

        mock_s3.list_objects.assert_called_once_with(Bucket=data_source.name, Prefix="prefix")

    def test_get_prefixes__match_func(self, data_source: S3DataSource):
        result = data_source.get_prefixes(re.compile("path1/(.+)"), match_func=lambda m: m.group(1))

        assert result == ["file1.json", "file2.json"]

    def test_read(self, data_source: S3DataSource, mock_read_parquet):
        mock_read_parquet.return_value = "data"
        expected_path = data_source.url("path")

        columns = ["col1", "col2", "col3"]
        filters = [("col1", "=", "val1")]

        result = data_source.read("path", columns=columns, filters=filters, extra1="extra1", extra2="extra2")

        assert result == "data"
        mock_read_parquet.assert_called_once_with(
            expected_path, columns=columns, filters=filters, extra1="extra1", extra2="extra2"
        )

    def test_url__no_path(self, data_source: S3DataSource):
        assert data_source.url() == f"s3://{data_source.name}"

    def test_url__with_path(self, data_source: S3DataSource):
        assert data_source.url("path1", "path2") == f"s3://{data_source.name}/path1/path2"
