import pandas as pd

from pems_data.cache import Cache
from pems_data.sources import IDataSource


class StationsService:
    """Manages fetching of station-related data."""

    @property
    def data_source(self) -> IDataSource:
        """This service's IDataSource instance."""
        return self._ds

    @property
    def imputation_detector_agg_5min(self) -> str:
        """
        Returns:
            value (str): The identifier for the imputation detector 5min aggregation
        """
        return "imputation/detector_imputed_agg_five_minutes"

    @property
    def metadata_file(self) -> str:
        """
        Returns:
            value (str): The identifier for the stations metadata file.
        """
        return "geo/current_stations.parquet"

    def __init__(self, data_source: IDataSource):
        """Initialize a new StationsService.

        Args:
            data_source (pems_data.sources.IDataSource): The data source responsible for fetching data for this service.
        """
        self._ds = data_source

    def _build_cache_key(self, *args):
        return Cache.build_key("stations", *args)

    def get_district_metadata(self, district_number: str) -> pd.DataFrame:
        """Loads metadata for all stations in the selected district from the data source.

        Args:
            district_number (str): The number of the Caltrans district to load metadata for, e.g. `"7"`.

        Returns:
            value (pandas.DataFrame): The station's data as a DataFrame.
        """

        cache_opts = {"key": self._build_cache_key("metadata", "district", district_number), "ttl": 3600}  # 1 hour
        columns = [
            "STATION_ID",
            "CONTROLLER_ID",
            "NAME",
            "PHYSICAL_LANES",
            "STATE_POSTMILE",
            "ABSOLUTE_POSTMILE",
            "LATITUDE",
            "LONGITUDE",
            "LENGTH",
            "STATION_TYPE",
            "DISTRICT",
            "FREEWAY",
            "DIRECTION",
            "COUNTY_NAME",
            "CITY_NAME",
        ]
        filters = [("DISTRICT", "=", district_number)]

        return self._ds.read(self.metadata_file, cache_opts=cache_opts, columns=columns, filters=filters)

    def get_imputed_agg_5min(self, station_id: str) -> pd.DataFrame:
        """Loads imputed aggregate 5 minute data for a specific station from the data source.

        Args:
            station_id (str): The identifier for the station/detector to load data, e.g. `"715898"`

        Returns:
            value (pandas.DataFrame): The station's data as a DataFrame.
        """

        cache_opts = {"key": self._build_cache_key("imputed", "agg", "5m", "station", station_id), "ttl": 3600}  # 1 hour
        columns = [
            "STATION_ID",
            "LANE",
            "SAMPLE_TIMESTAMP",
            "VOLUME_SUM",
            "SPEED_FIVE_MINS",
            "OCCUPANCY_AVG",
        ]
        filters = [("STATION_ID", "=", station_id)]

        return self._ds.read(self.imputation_detector_agg_5min, cache_opts=cache_opts, columns=columns, filters=filters)
