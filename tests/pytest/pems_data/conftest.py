import pandas as pd
import pytest


@pytest.fixture
def df() -> pd.DataFrame:
    return pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
