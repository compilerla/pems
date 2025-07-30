from abc import ABC, abstractmethod
from typing import Any

import pandas as pd


class IDataSource(ABC):
    """An abstract interface for a generic data source."""

    @abstractmethod
    def read(self, identifier: str, **kwargs: dict[str, Any]) -> pd.DataFrame:
        """
        Reads data identified by a generic identifier from the source.

        Args:
            identifier (str): The unique identifier for the data, e.g., an S3 key, a database table name, etc.
            **kwargs (dict[str, Any]): Additional arguments for the underlying read operation, such as 'columns' or 'filters'.

        Returns:
            value (pandas.DataFrame): A DataFrame of data from the source for the given identifier.
        """
        raise NotImplementedError  # pragma: no cover
