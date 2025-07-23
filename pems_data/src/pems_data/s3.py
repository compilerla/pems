import re

import boto3
import pandas as pd


class S3Bucket:
    prod_marts = "caltrans-pems-prd-us-west-2-marts"

    def __init__(self, name: str = None):
        self.name = name or self.prod_marts

    def get_prefixes(self, filter_pattern: re.Pattern = re.compile(".+"), initial_prefix: str = "", match_func=None) -> list:
        """
        Lists available filter options by inspecting S3 prefixes. Optionally filter by an initial prefix.

        When a match is found, if match_func exists, add its result to the output list. Otherwise add the entire match.
        """

        s3 = boto3.client("s3")
        s3_keys = s3.list_objects(Bucket=self.name, Prefix=initial_prefix)

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

    def read_parquet(self, *args, path=None, columns=None, filters=None, **kwargs) -> pd.DataFrame:
        """Reads data from the S3 path into a pandas DataFrame. Extra kwargs are pass along to `pandas.read_parquet()`.

        Args:
            *args (str): One or more path relative path components for the data file.
            path (str): The absolute S3 URL path to a data file. Using `path` overrides any relative path components provided.
            columns (list[str]): If not None, only these columns will be read from the file.
            filters (list[tuple] | list[list[tuple]]): To filter out data. Filter syntax: `[[(column, op, val), ...],...]`.
        """
        path = path or self.url(*args)
        return pd.read_parquet(path, columns=columns, filters=filters, **kwargs)

    def url(self, *args):
        """Build an absolute S3 URL to this bucket, with optional path segments."""
        parts = [f"s3://{self.name}"]
        parts.extend(args)
        return "/".join(parts)
