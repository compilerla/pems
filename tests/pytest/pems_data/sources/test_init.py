import pandas as pd
import pytest

from pems_data.sources import IDataSource


class TestIDataSource:

    def test_cannot_instantiate_abstract(self):
        """Test that IDataSource cannot be instantiated directly"""
        with pytest.raises(TypeError, match=r"Can't instantiate abstract class IDataSource"):
            IDataSource()

    def test_must_implement_read(self):
        """Test that concrete classes must implement read method"""

        class InvalidSource(IDataSource):
            pass

        with pytest.raises(TypeError, match=r"Can't instantiate abstract class InvalidSource"):
            InvalidSource()

    def test_valid_implementation(self):
        """Test that a valid implementation can be instantiated and used"""

        class ValidSource(IDataSource):
            def read(self, identifier: str, **kwargs) -> pd.DataFrame:
                return pd.DataFrame({"test": [1, 2, 3]})

        source = ValidSource()
        result = source.read("test-id", columns=["col1"])

        assert isinstance(result, pd.DataFrame)
        assert not result.empty
        assert result.equals(pd.DataFrame({"test": [1, 2, 3]}))
