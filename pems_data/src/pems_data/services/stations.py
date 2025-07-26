import pandas as pd

from pems_data.sources import IDataSource


class StationsService:
    """Manages fetching of station-related data."""

    imputation_detector_agg_5min = "imputation/detector_imputed_agg_five_minutes"
    metadata_file = "geo/current_stations.parquet"

    def __init__(self, data_source: IDataSource):
        self.data_source = data_source

    def get_district_metadata(self, district_number: str) -> pd.DataFrame:
        """Loads metadata for all stations in the selected District from S3."""

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

        return self.data_source.read(self.metadata_file, columns=columns, filters=filters)

    def get_imputed_agg_5min(self, station_id: str) -> pd.DataFrame:
        """Loads imputed aggregate 5 minute data for a specific station."""

        columns = [
            "STATION_ID",
            "LANE",
            "SAMPLE_TIMESTAMP",
            "VOLUME_SUM",
            "SPEED_FIVE_MINS",
            "OCCUPANCY_AVG",
        ]
        filters = [("STATION_ID", "=", station_id)]

        return self.data_source.read(self.imputation_detector_agg_5min, columns=columns, filters=filters)
