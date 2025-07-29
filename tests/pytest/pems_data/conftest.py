import pandas as pd
import pytest


@pytest.fixture
def df() -> pd.DataFrame:
    return pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})


@pytest.fixture(autouse=True)
def mock_s3(mocker):
    s3 = mocker.patch("boto3.client").return_value
    s3.list_objects.return_value = {
        "Contents": [
            {"Key": "path1/file2.json"},
            {"Key": "path2/file1.json"},
            {"Key": "path1/file1.json"},
        ]
    }
    return s3
