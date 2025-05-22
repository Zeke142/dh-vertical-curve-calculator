import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

st.set_page_config(page_title="Vertical Curve Calculator", layout="centered")

st.title("Vertical Curve Calculator")

input_mode = st.radio("Choose Input Method:", ("Elevation-Based", "Grade-Based"))

if input_mode == "Elevation-Based":
    st.subheader("Elevation-Based Inputs")
    bvc_station = st.number_input("BVC Station", step=1.0, format="%.2f")
    bvc_elevation = st.number_input("BVC Elevation", step=0.01)
    evc_station = st.number_input("EVC Station", step=1.0, format="%.2f")
    evc_elevation = st.number_input("EVC Elevation", step=0.01)
    pvi_station = st.number_input("PVI Station", value=(bvc_station + evc_station) / 2, step=1.0, format="%.2f")
    pvi_elevation = st.number_input("PVI Elevation", step=0.01)

    curve_length = evc_station - bvc_station
    g1 = ((pvi_elevation - bvc_elevation) / (pvi_station - bvc_station) * 100) if pvi_station != bvc_station else 0.0
    g2 = ((evc_elevation - pvi_elevation) / (evc_station - pvi_station) * 100) if evc_station != pvi_station else 0.0

else:
    st.subheader("Grade-Based Inputs")
    bvc_station = st.number_input("BVC Station", step=1.0, format="%.2f")
    evc_station = st.number_input("EVC Station", step=1.0, format="%.2f")
    bvc_elevation = st.number_input("BVC Elevation", step=0.01)
    g1 = st.number_input("Grade In (g₁) [%]", step=0.01, format="%.2f")
    g2 = st.number_input("Grade Out (g₂) [%]", step=0.01, format="%.2f")
    pvi_station = (bvc_station + evc_station) / 2
    curve_length = evc_station - bvc_station
    pvi_elevation = bvc_elevation + (g1 / 100) * (pvi_station - bvc_station)

a_value = g2 - g1

use_custom_k = st.checkbox("Enter custom K-value?")
if use_custom_k:
    k_value = st.number_input("K-value", step=0.01)
else:
    k_value = curve_length / abs(a_value) if a_value != 0 else None

st.header("Results")
st.markdown(f"**Curve Length (L):** {curve_length:.4f} ft")
st.markdown(f"**Grade In (g₁):** {g1:.4f} %")
st.markdown(f"**Grade Out (g₂):** {g2:.4f} %")
st.markdown(f"**A = g₂ - g₁:** {a_value:.4f} %")
if k_value is not None:
    st.markdown(f"**K-value:** {k_value:.4f}")
else:
    st.markdown("**K-value:** Undefined (division by zero)")

st.subheader("Elevation at Any Station")
station_input = st.number_input("Enter Station", step=1.0, format="%.2f")

if bvc_station <= station_input <= evc_station:
    x = station_input - bvc_station
    g1_decimal = g1 / 100
    elevation = bvc_elevation + g1_decimal * x + (a_value / 100) * x**2 / (2 * curve_length)
    grade_at_x = g1 + (a_value * x / curve_length)
    st.markdown(f"**Elevation at station {station_input:.2f}:** {elevation:.4f} ft")
    st.markdown(f"**Grade at station {station_input:.2f}:** {grade_at_x:.4f} %")
else:
    elevation = None
    st.warning("Station is outside the limits of the vertical curve.")

st.subheader("Vertical Curve Profile")

if curve_length > 0:
    x_vals = np.arange(0, curve_length + 1, 1)
    g1_decimal = g1 / 100
    y_vals = bvc_elevation + g1_decimal * x_vals + (a_value / 100) * x_vals**2 / (2 * curve_length)
    df = pd.DataFrame({
        "Station": x_vals + bvc_station,
        "Elevation": y_vals
    })

    label_data = pd.DataFrame({
        "Station": [bvc_station, pvi_station, evc_station],
        "Elevation": [bvc_elevation, pvi_elevation, evc_elevation],
        "Label": ["BVC", "PVI", "EVC"]
    })

    line = alt.Chart(df).mark_line().encode(
        x=alt.X("Station", title="Station"),
        y=alt.Y("Elevation", title="Elevation")
    )

    points = alt.Chart(label_data).mark_point(filled=True, size=100).encode(
        x="Station", y="Elevation", color=alt.Color("Label", legend=None),
        tooltip=["Label", "Station", "Elevation"]
    )

    labels = alt.Chart(label_data).mark_text(
        align='left', baseline='bottom', dx=5
    ).encode(
        x='Station',
        y='Elevation',
        text='Label'
    )

    chart_layers = [line, points, labels]

    if elevation is not None:
        design_df = pd.DataFrame({
            "Station": [station_input],
            "Elevation": [elevation],
            "Label": ["Design Point"]
        })

        design_marker = alt.Chart(design_df).mark_point(filled=True, size=100).encode(
            x="Station", y="Elevation", color=alt.value("red"),
            tooltip=["Label", "Station", "Elevation"]
        )

        design_label = alt.Chart(design_df).mark_text(
            align='left', baseline='top', dx=5, dy=15
        ).encode(
            x='Station',
            y='Elevation',
            text=alt.Text("Station", format=".2f")
        )

        elev_label = alt.Chart(design_df).mark_text(
            align='left', baseline='top', dx=5, dy=30
        ).encode(
            x='Station',
            y='Elevation',
            text=alt.Text("Elevation", format=".2f")
        )

        chart_layers.extend([design_marker, design_label, elev_label])

    chart = alt.layer(*chart_layers).properties(
        width=700,
        height=400,
        title="Vertical Curve Profile"
    )

    st.altair_chart(chart, use_container_width=True)
else:
    st.info("Please enter valid BVC and EVC stations to generate the graph.")