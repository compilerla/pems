import pandas as pd

from pems_data.s3 import S3Bucket


class StationsBucket(S3Bucket):
    """Station-specific bucket data."""

    imputation_detector_agg_5min = "imputation/detector_imputed_agg_five_minutes"
    metadata_file = "geo/current_stations.parquet"

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

        return self.read_parquet(self.metadata_file, columns=columns, filters=filters)

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

        return self.read_parquet(self.imputation_detector_agg_5min, columns=columns, filters=filters)
