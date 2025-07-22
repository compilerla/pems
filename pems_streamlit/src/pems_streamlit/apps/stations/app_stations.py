import re

import pandas as pd
import streamlit as st

from pems_data import ServiceFactory

from pems_streamlit.components.map_station_summary import map_station_summary

FACTORY = ServiceFactory()
STATIONS = FACTORY.stations_service()
S3 = FACTORY.s3_source


@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_station_metadata(district_number: str) -> pd.DataFrame:
    """Loads metadata for all stations in the selected District from S3."""
    return STATIONS.get_district_metadata(district_number)


@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_available_days() -> set:
    """
    Lists available days by inspecting S3 prefixes.
    """
    # Find "day=", then capture one or more digits that immediately follow it
    pattern = re.compile(r"day=(\d+)")

    # add as int only the text captured by the first set of parentheses to the set
    def match(m: re.Match):
        return int(m.group(1))

    return S3.get_prefixes(pattern, initial_prefix=STATIONS.imputation_detector_agg_5min, match_func=match)


@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_station_data(station_id: str) -> pd.DataFrame:
    """
    Loads station data for a specific station.
    """
    return STATIONS.get_imputed_agg_5min(station_id)


# --- STREAMLIT APP ---


def main():
    query_params = st.query_params
    district_number = query_params.get("district_number", "")

    df_station_metadata = load_station_metadata(district_number)

    map_placeholder = st.empty()

    station = st.selectbox(
        "Station",
        df_station_metadata["STATION_ID"],
    )

    with map_placeholder:
        df_selected_station = df_station_metadata.query("STATION_ID == @station")
        map_station_summary(df_selected_station)

    days = st.multiselect("Days", get_available_days())

    station_data_button = st.button("Load Station Data", type="primary")

    if station_data_button:
        df_station_data = load_station_data(station)
        st.dataframe(df_station_data, use_container_width=True)


if __name__ == "__main__":
    main()
