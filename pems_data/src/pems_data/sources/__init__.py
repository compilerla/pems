from abc import ABC, abstractmethod

import pandas as pd


class IDataSource(ABC):
    """
    An abstract interface for a generic data source.
    """

    @abstractmethod
    def read(self, identifier: str, **kwargs) -> pd.DataFrame:
        """
        Reads data identified by a generic identifier from the source.

        Args:
            identifier (str): The unique identifier for the data, e.g.,
                              an S3 key, a database table name, etc.
            **kwargs: Additional arguments for the underlying read operation,
                      such as 'columns' or 'filters'.
        """
        raise NotImplementedError  # pragma: no cover
