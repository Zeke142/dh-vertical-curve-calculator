import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Vertical Curve Calculator", layout="wide")

st.title("Vertical Curve Calculator")

# --- User Inputs ---
st.sidebar.header("Input Parameters")

bvc_station = st.sidebar.number_input("BVC Station (ft)", value=1000.00)
bvc_elevation = st.sidebar.number_input("BVC Elevation (ft)", value=500.00)
pvi_station = st.sidebar.number_input("PVI Station (ft)", value=1100.00)
pvi_elevation = st.sidebar.number_input("PVI Elevation (ft)", value=510.00)
g1 = st.sidebar.number_input("Initial Grade g₁ (%)", value=1.0)
g2 = st.sidebar.number_input("Final Grade g₂ (%)", value=-1.0)

station_input = st.sidebar.number_input("Query Station (ft)", value=1050.00)

# --- Derived Values ---
curve_length = abs(pvi_station - bvc_station) * 2
evc_station = bvc_station + curve_length
a_value = g2 - g1  # Algebraic difference in grades

# --- Elevation Calculation ---
st.subheader("Elevation at a Given Station")

x = station_input - bvc_station
station_within_limits = bvc_station <= station_input <= evc_station

elevation = None
grade_at_x = None

if station_within_limits:
    g1_decimal = g1 / 100
    elevation = bvc_elevation + g1_decimal * x + (a_value / 100) * x**2 / (2 * curve_length)
    grade_at_x = g1  # Keep this fixed as per your model
    st.markdown(f"**Elevation at station {station_input:.2f}:** {elevation:.4f} ft")
    st.markdown(f"**Grade at station {station_input:.2f}:** {grade_at_x:.4f} %")
else:
    st.warning("Station is outside the limits of the vertical curve.")

# --- Vertical Curve Profile ---
st.subheader("Vertical Curve Profile")

if curve_length > 0:
    x_vals = np.arange(0, curve_length + 1, 1)
    g1_decimal = g1 / 100
    y_vals = bvc_elevation + g1_decimal * x_vals + (a_value / 100) * x_vals**2 / (2 * curve_length)

    df = pd.DataFrame({
        "Station (ft)": x_vals + bvc_station,
        "Elevation (ft)": y_vals
    })

    # Dynamic Y-axis range
    y_min = np.floor(min(y_vals)) - 1
    y_max = np.ceil(max(y_vals)) + 1
    y_range = [y_min, y_max]

    # Label data
    elevations = [round(bvc_elevation, 2), round(pvi_elevation, 2), round(evc_elevation, 2)]
    stations = [round(bvc_station, 2), round(pvi_station, 2), round(evc_station, 2)]
    labels = [
        f"BVC (g₁ = {g1:.2f}%)",
        f"PVI\nSta: {pvi_station:.2f}\nElev: {pvi_elevation:.2f}",
        f"EVC (g₂ = {g2:.2f}%)"
    ]

    if elevation is not None:
        elevations.append(round(elevation, 2))
        stations.append(round(station_input, 2))
        labels.append(f"Station {station_input:.2f}")

    label_df = pd.DataFrame({
        "Station (ft)": stations,
        "Elevation (ft)": elevations,
        "Label": labels
    })

    # --- Plotting ---
    import altair as alt

    base = alt.Chart(df).mark_line().encode(
        x=alt.X("Station (ft)", scale=alt.Scale(zero=False)),
        y=alt.Y("Elevation (ft)", scale=alt.Scale(domain=y_range)),
        tooltip=["Station (ft)", "Elevation (ft)"]
    ).properties(title="Vertical Curve Profile")

    points = alt.Chart(label_df).mark_point(color="red", size=60).encode(
        x="Station (ft)",
        y="Elevation (ft)",
        tooltip=["Label", "Station (ft)", "Elevation (ft)"]
    )

    text = alt.Chart(label_df).mark_text(
        align='left',
        dx=5,
        dy=-10,
        fontSize=12
    ).encode(
        x="Station (ft)",
        y="Elevation (ft)",
        text="Label"
    )

    st.altair_chart(base + points + text, use_container_width=True)
else:
    st.warning("Invalid curve length. Please check your inputs.")