from pathlib import Path

import pandas as pd
import streamlit as st
from pygwalker.api.streamlit import StreamlitRenderer

APP_DIR = Path(__file__).parent

st.set_page_config(layout="wide")


@st.cache_data()
def fetch_data():
    data = pd.read_csv("https://kanaries-app.s3.ap-northeast-1.amazonaws.com/public-datasets/bike_sharing_dc.csv")
    return data


@st.cache_data()
def fetch_config():
    data = Path(APP_DIR / "pygwalker.json").read_text()
    return data


df = fetch_data()
vis_spec = fetch_config()

pyg_app = StreamlitRenderer(df, spec=vis_spec)
pyg_app.explorer()
