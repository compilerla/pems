import re

import pandas as pd
import streamlit as st

from pems_data import ServiceFactory

from pems_streamlit.components.map_station_summary import map_station_summary
from pems_streamlit.components.plot_5_min_traffic_data import plot_5_min_traffic_data

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

    quantity = st.multiselect("Quantity", ["VOLUME_SUM", "OCCUPANCY_AVG", "SPEED_FIVE_MINS"])

    num_lanes = int(df_station_metadata[df_station_metadata["STATION_ID"] == station]["PHYSICAL_LANES"].iloc[0])
    lane = st.multiselect(
        "Lane",
        list(range(1, num_lanes + 1)),
    )

    with map_placeholder:
        df_selected_station = df_station_metadata.query("STATION_ID == @station")
        map_station_summary(df_selected_station)

    days = st.multiselect("Days", get_available_days())

    station_data_button = st.button("Load Station Data", type="primary")

    error_placeholder = st.empty()
    plot_placeholder = st.empty()

    if station_data_button:
        error_messages = []
        if len(quantity) == 0 or len(quantity) > 2:
            error_messages.append("- Please select one or two quantities to proceed.")
        if not lane:
            error_messages.append("- Please select at least one lane to proceed.")
        if not days:
            error_messages.append("- Please select at least one day to proceed.")
        if error_messages:
            full_error_message = "\n".join(error_messages)
            error_placeholder.error(full_error_message)
        else:
            df_station_data = load_station_data(station)
            filtered_df = df_station_data[
                (df_station_data["SAMPLE_TIMESTAMP"].dt.day.isin(days)) & (df_station_data["LANE"].isin(lane))
            ]
            filtered_df_sorted = filtered_df.sort_values(by="SAMPLE_TIMESTAMP")

            fig = plot_5_min_traffic_data(filtered_df_sorted, quantity, lane)
            plot_placeholder.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
