import pandas as pd

from pems_data.cache import Cache
from pems_data.sources import IDataSource


class StationsService:
    """Manages fetching of station-related data."""

    imputation_detector_agg_5min = "imputation/detector_imputed_agg_five_minutes"
    metadata_file = "geo/current_stations.parquet"

    def __init__(self, data_source: IDataSource):
        self.data_source = data_source

    def _build_cache_key(self, *args):
        return Cache.build_key("stations", *args)

    def get_district_metadata(self, district_number: str) -> pd.DataFrame:
        """Loads metadata for all stations in the selected District from S3."""

        cache_opts = {"key": self._build_cache_key("metadata", "district", district_number), "ttl": 3600}  # 1 hour
        columns = [
            "STATION_ID",
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

        return self.data_source.read(self.metadata_file, cache_opts=cache_opts, columns=columns, filters=filters)

    def get_imputed_agg_5min(self, station_id: str) -> pd.DataFrame:
        """Loads imputed aggregate 5 minute data for a specific station."""

        cache_opts = {"key": self._build_cache_key("imputed", "agg", "5m", "station", station_id), "ttl": 300}  # 5 minutes
        columns = [
            "STATION_ID",
            "LANE",
            "SAMPLE_TIMESTAMP",
            "VOLUME_SUM",
            "SPEED_FIVE_MINS",
            "OCCUPANCY_AVG",
        ]
        filters = [("STATION_ID", "=", station_id)]

        return self.data_source.read(
            self.imputation_detector_agg_5min, cache_opts=cache_opts, columns=columns, filters=filters
        )
