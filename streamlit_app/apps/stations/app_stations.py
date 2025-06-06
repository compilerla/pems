from pathlib import Path

import os
import pandas as pd
import streamlit as st


APP_DIR = Path(__file__).parent


@st.cache_data()
def fetch_data():
    all_files = os.listdir(APP_DIR)
    # Get station metadata files
    station_files = [f for f in all_files if "_text_meta_" in f and f.endswith(".txt")]

    df_list = []
    for f in station_files:
        file_path = os.path.join(APP_DIR, f)
        df = pd.read_csv(file_path, delimiter="\t")
        df_list.append(df)
    # Combine into a single DataFrame
    df_all = pd.concat(df_list, ignore_index=True)

    data = df_all.dropna(subset=["Latitude", "Longitude"])
    data.loc[:, "State_PM"] = data["State_PM"].astype(str)
    data.loc[:, "User_ID_1"] = data["User_ID_1"].astype(str)
    return data


query_params = st.query_params
district_number = query_params.get("district_number", "")
district_number = int(district_number) if district_number else district_number  # Ensure district_number is an integer

st.set_page_config(layout="wide")

df = fetch_data()
if district_number:
    # filter to just the current district
    df = df[df["District"] == district_number]
    st.title(f"District {district_number} Station Viewer")
else:
    st.title("Districts Station Viewer")

left_col, center_col, right_col = st.columns([1, 2, 2])

with left_col:
    # Create filters
    id_options = ["All"] + sorted(df["ID"].dropna().unique().tolist())
    selected_id = st.selectbox("Select Station", id_options)

    fwy_options = ["All"] + sorted(df["Fwy"].dropna().unique().tolist())
    selected_fwy = st.selectbox("Select Freeway", fwy_options)

    dir_options = ["All"] + sorted(df["Dir"].dropna().unique().tolist())
    selected_dir = st.selectbox("Select Direction", dir_options)

    type_options = ["All"] + sorted(df["Type"].dropna().unique().tolist())
    selected_type = st.selectbox("Select Type", type_options)

# Apply filters
filtered_df = df.copy()

if selected_id != "All":
    filtered_df = filtered_df[filtered_df["ID"] == selected_id]

if selected_fwy != "All":
    filtered_df = filtered_df[filtered_df["Fwy"] == selected_fwy]

if selected_dir != "All":
    filtered_df = filtered_df[filtered_df["Dir"] == selected_dir]

if selected_type != "All":
    filtered_df = filtered_df[filtered_df["Type"] == selected_type]

with center_col:
    # Show filtered data
    st.write(f"**Stations:** {filtered_df.shape[0]:,.0f}")
    st.write(f"**Directional distance:** {filtered_df["Length"].sum():,.1f} mi")
    st.dataframe(filtered_df, use_container_width=True)

with right_col:
    # Rename columns to match Streamlit's expected format
    map_df = filtered_df.rename(columns={"Latitude": "latitude", "Longitude": "longitude"})
    st.map(map_df[["latitude", "longitude"]])
