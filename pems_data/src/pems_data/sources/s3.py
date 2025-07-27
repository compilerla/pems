import os
import re
from typing import Any, Callable

import boto3
import pandas as pd

from pems_data.sources import IDataSource


class S3DataSource(IDataSource):
    """A data source for fetching data from an S3 bucket."""

    @property
    def default_bucket(self) -> str:
        """
        Returns:
            value (str): The value from the `S3_BUCKET_NAME` environment variable, or the Caltrans PeMS prod mart bucket name.
        """
        return os.environ.get("S3_BUCKET_NAME", "caltrans-pems-prd-us-west-2-marts")

    @property
    def name(self) -> str:
        """
        Returns:
            value (str): The name of this bucket instance.
        """
        return self._name

    def __init__(self, name: str = None):
        """Initialize a new S3DataSource.

        Args:
            name (str): (Optional) The name of the S3 bucket to source from.
        """
        self._client = boto3.client("s3")
        self._name = name or self.default_bucket

    def get_prefixes(
        self,
        filter_pattern: re.Pattern = re.compile(".+"),
        initial_prefix: str = "",
        match_func: Callable[[re.Match], str] = None,
    ) -> list:
        """
        Lists available object prefixes, optionally filtered by an initial prefix.

        When a match is found, if match_func exists, add its result to the output list. Otherwise add the entire match.

        Args:
            filter_pattern (re.Pattern): A regular expression used to match object prefixes
            initial_prefix (str): The initial prefix to start the search from
            match_func (Callable[[re.Match], str]): A callable used to extract data from prefix matches

        Returns:
            value (list): A sorted list of unique prefixes that matched the pattern.
        """

        s3_keys = self._client.list_objects(Bucket=self.name, Prefix=initial_prefix)

        result = set()

        for item in s3_keys["Contents"]:
            s3_path = item["Key"]
            match = re.search(filter_pattern, s3_path)
            if match:
                if match_func:
                    result.add(match_func(match))
                else:
                    result.add(match.group(0))

        return sorted(result)

    def read(
        self, *args: str, path: str = None, columns: list = None, filters: list = None, **kwargs: dict[str, Any]
    ) -> pd.DataFrame:
        """Reads data from the S3 path into a pandas DataFrame. Extra kwargs are passed along to `pandas.read_parquet()`.

        Args:
            *args (tuple[str]): One or more path relative path components for the data file
            path (str): The absolute S3 URL path to a data file; using `path` overrides any relative path components provided
            columns (list[str]): If not None, only these columns will be read from the file
            filters (list[tuple] | list[list[tuple]]): To filter out data. Filter syntax: `[[(column, op, val), ...],...]`
            **kwargs (dict[str, Any]): Extra kwargs to pass to `pandas.read_parquet()`

        Returns:
            value (pandas.DataFrame): A DataFrame of data read from the source path.
        """
        path = path or self.url(*args)
        return pd.read_parquet(path, columns=columns, filters=filters, **kwargs)

    def url(self, *args: str) -> str:
        """Build an absolute S3 URL to this bucket, with optional path segments.

        Args:
            *args (tuple[str]): The components of the S3 path.

        Returns:
            value (str): An absolute `s3://` URL for this bucket and the path.
        """
        parts = [f"s3://{self.name}"]
        parts.extend(args)
        return "/".join(parts)
