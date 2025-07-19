import pandas as pd

from pems_data.stations import StationsBucket
import pytest


class TestStationsBucket:
    @pytest.fixture
    def df(self):
        return pd.DataFrame({"STATION_ID": [1]})

    @pytest.fixture
    def mock_read_parquet(self, df, mocker):
        return mocker.patch("pems_data.stations.StationsBucket.read_parquet", return_value=df)

    @pytest.fixture
    def bucket(self):
        return StationsBucket()

    def test_imputation_detector_agg_5min(self):
        assert StationsBucket.imputation_detector_agg_5min == "imputation/detector_imputed_agg_five_minutes"

    def test_metadata_file(self):
        assert StationsBucket.metadata_file == "geo/current_stations.parquet"

    def test_get_district_metadata(self, bucket: StationsBucket, df, mock_read_parquet):
        district_number = "7"
        result = bucket.get_district_metadata(district_number)

        mock_read_parquet.assert_called_once_with(
            StationsBucket.metadata_file,
            columns=[
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
            ],
            filters=[("DISTRICT", "=", district_number)],
        )
        assert result.equals(df)

    def test_get_imputed_agg_5min(self, bucket: StationsBucket, df, mock_read_parquet):
        station_id = "123"

        result = bucket.get_imputed_agg_5min(station_id)

        mock_read_parquet.assert_called_once_with(
            StationsBucket.imputation_detector_agg_5min,
            columns=[
                "STATION_ID",
                "LANE",
                "SAMPLE_TIMESTAMP",
                "VOLUME_SUM",
                "SPEED_FIVE_MINS",
                "OCCUPANCY_AVG",
            ],
            filters=[("STATION_ID", "=", station_id)],
        )
        assert result.equals(df)
