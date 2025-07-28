import pandas as pd
import pytest

from pems_data.sources import IDataSource
from pems_data.services.stations import StationsService


class TestStationsService:
    @pytest.fixture
    def df(self):
        return pd.DataFrame({"STATION_ID": [1]})

    @pytest.fixture
    def data_source(self, df, mocker):
        mock = mocker.Mock(spec=IDataSource)
        mock.read.return_value = df
        return mock

    @pytest.fixture
    def service(self, data_source):
        return StationsService(data_source)

    def test_imputation_detector_agg_5min(self):
        assert StationsService.imputation_detector_agg_5min == "imputation/detector_imputed_agg_five_minutes"

    def test_metadata_file(self):
        assert StationsService.metadata_file == "geo/current_stations.parquet"

    def test_get_district_metadata(self, service: StationsService, data_source: IDataSource, df):
        district_number = "7"
        result = service.get_district_metadata(district_number)

        data_source.read.assert_called_once()
        assert data_source.read.call_args.args[0] == StationsService.metadata_file
        assert data_source.read.call_args.kwargs["columns"] == [
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
        assert data_source.read.call_args.kwargs["filters"] == [("DISTRICT", "=", district_number)]

        pd.testing.assert_frame_equal(result, df)

    def test_get_imputed_agg_5min(self, service: StationsService, data_source: IDataSource, df):
        station_id = "123"

        result = service.get_imputed_agg_5min(station_id)

        data_source.read.assert_called_once()
        assert data_source.read.call_args.args[0] == StationsService.imputation_detector_agg_5min
        assert data_source.read.call_args.kwargs["columns"] == [
            "STATION_ID",
            "LANE",
            "SAMPLE_TIMESTAMP",
            "VOLUME_SUM",
            "SPEED_FIVE_MINS",
            "OCCUPANCY_AVG",
        ]
        assert data_source.read.call_args.kwargs["filters"] == [("STATION_ID", "=", station_id)]

        pd.testing.assert_frame_equal(result, df)
