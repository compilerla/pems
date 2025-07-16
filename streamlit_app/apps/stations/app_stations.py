import re
import boto3
import pandas as pd
import streamlit as st

S3_BUCKET = "caltrans-pems-prd-us-west-2-marts"
STATIONS_METADATA_KEY = "geo/current_stations.parquet"
DATA_PREFIX = "imputation/detector_imputed_agg_five_minutes"


@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_station_metadata(district_number: str) -> pd.DataFrame:
    """Loads metadata for all stations in the selected District from S3."""

    filters = [("DISTRICT", "=", district_number)]

    return pd.read_parquet(
        f"s3://{S3_BUCKET}/{STATIONS_METADATA_KEY}",
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
        filters=filters,
    )


@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_available_days() -> set:
    """
    Lists available days by inspecting S3 prefixes.
    """

    s3 = boto3.client("s3")
    s3_keys = s3.list_objects(Bucket=S3_BUCKET, Prefix=DATA_PREFIX)

    days = set()

    for item in s3_keys["Contents"]:
        s3_path = item["Key"]
        # Find "day=", then capture one or more digits that immediately follow it
        match = re.search(r"day=(\d+)", s3_path)
        if match:
            # add as int only the text captured by the first set of parentheses to the set
            days.add(int(match.group(1)))

    return sorted(days)


# --- STREAMLIT APP ---

query_params = st.query_params
district_number = query_params.get("district_number", "")

df_station_metadata = load_station_metadata(district_number)
st.dataframe(df_station_metadata, use_container_width=True)

station = st.selectbox(
    "Station",
    df_station_metadata["STATION_ID"],
)

days = st.multiselect("Days", get_available_days())
