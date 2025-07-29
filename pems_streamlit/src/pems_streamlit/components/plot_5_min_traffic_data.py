import pandas as pd
import plotly.graph_objs as go
import streamlit as st

QUANTITY_CONFIG = {
    "VOLUME_SUM": {"name": "Volume (veh/hr)"},
    "OCCUPANCY_AVG": {"name": "Occupancy (%)"},
    "SPEED_FIVE_MINS": {"name": "Speed (mph)"},
}


def plot_5_min_traffic_data(df_station_data: pd.DataFrame, quantities: list, lanes: list):
    fig = go.Figure()

    layout_updates = {
        "xaxis": dict(title="Time of Day"),
        "legend": dict(orientation="h", yanchor="top", y=-0.3, xanchor="center", x=0.5),
    }

    # One quantity selected
    if len(quantities) == 1:
        qty_key = quantities[0]
        qty_name = QUANTITY_CONFIG[qty_key]["name"]

        for lane in lanes:
            df_lane = df_station_data[df_station_data["LANE"] == lane]
            fig.add_trace(
                go.Scatter(
                    x=df_lane["SAMPLE_TIMESTAMP"],
                    y=df_lane[qty_key],
                    mode="lines",
                    name=f"Lane {lane} {qty_name.split(' ')[0]}",
                )
            )

        layout_updates["title"] = dict(text=f"<b>{qty_name}</b>", x=0.5, xanchor="center")
        layout_updates["yaxis"] = dict(title=f"<b>{qty_name}</b>", side="left")

    # Two quantities selected
    elif len(quantities) == 2:
        left_qty_key, right_qty_key = quantities[0], quantities[1]
        left_qty_name = QUANTITY_CONFIG[left_qty_key]["name"]
        right_qty_name = QUANTITY_CONFIG[right_qty_key]["name"]

        for lane in lanes:
            df_lane = df_station_data[df_station_data["LANE"] == lane]
            fig.add_trace(
                go.Scatter(
                    x=df_lane["SAMPLE_TIMESTAMP"],
                    y=df_lane[left_qty_key],
                    mode="lines",
                    name=f"Lane {lane} {left_qty_name.split(' ')[0]}",
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=df_lane["SAMPLE_TIMESTAMP"],
                    y=df_lane[right_qty_key],
                    mode="lines",
                    name=f"Lane {lane} {right_qty_name.split(' ')[0]}",
                    yaxis="y2",
                )
            )

        # Create layout for two axes
        layout_updates["title"] = dict(text=f"<b>{left_qty_name} vs. {right_qty_name}</b>", x=0.5, xanchor="center")
        layout_updates["yaxis"] = dict(title=f"<b>{left_qty_name}</b>", side="left")
        layout_updates["yaxis2"] = dict(title=f"<b>{right_qty_name}</b>", side="right", overlaying="y")

    fig.update_layout(**layout_updates)

    st.plotly_chart(fig, use_container_width=True)
