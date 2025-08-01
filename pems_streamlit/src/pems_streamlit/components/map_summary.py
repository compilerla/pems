import pandas as pd
import streamlit as st


def map_district_summary(df_station_metadata: pd.DataFrame):

    map_col, info_col = st.columns([0.6, 0.4])

    with map_col:
        map_df = df_station_metadata.rename(columns={"LATITUDE": "latitude", "LONGITUDE": "longitude"})
        map_df_cleaned = map_df.dropna(subset=["latitude", "longitude"])
        st.map(map_df_cleaned[["latitude", "longitude"]], height=265)

    with info_col:
        with st.container(border=True):
            st.markdown(f"**Directional Distance** {df_station_metadata['LENGTH'].sum().round(1)} miles")
            st.markdown(f"**Freeways** {df_station_metadata['FREEWAY'].nunique()}")
            st.markdown(f"**Stations** {df_station_metadata['STATION_ID'].nunique()}")
            st.markdown(f"**Controllers** {df_station_metadata['CONTROLLER_ID'].nunique()}")


def map_station_summary(df_station_metadata: pd.DataFrame):

    map_col, info_col = st.columns([0.6, 0.4])

    with map_col:
        map_df = df_station_metadata.rename(columns={"LATITUDE": "latitude", "LONGITUDE": "longitude"})
        map_df_cleaned = map_df.dropna(subset=["latitude", "longitude"])
        st.map(map_df_cleaned[["latitude", "longitude"]], height=265)

    with info_col:
        with st.container(border=True):
            st.markdown(f"**Station {df_station_metadata['STATION_ID'].item()} - {df_station_metadata['NAME'].item()}**")
            st.markdown(
                f"{df_station_metadata["FREEWAY"].item()} - {df_station_metadata["DIRECTION"].item()}, {df_station_metadata["CITY_NAME"].item()}"
            )
            st.markdown(f"**County** {df_station_metadata["COUNTY_NAME"].item()}")
            st.markdown(f"**District** {df_station_metadata["DISTRICT"].item()}")
            st.markdown(f"**Absolute Post Mile** {df_station_metadata["ABSOLUTE_POSTMILE"].item()}")
            st.markdown(f"**Lanes** {df_station_metadata["PHYSICAL_LANES"].item()}")
