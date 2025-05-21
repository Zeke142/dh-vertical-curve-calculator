import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

st.set_page_config(page_title="Vertical Curve Calculator", layout="centered")
st.title("Vertical Curve Calculator")

# --- Input Parameters ---
st.sidebar.header("Input Parameters")
bvc_station = st.sidebar.number_input("BVC Station (ft)", value=1850.00, step=0.01)
bvc_elevation = st.sidebar.number_input("BVC Elevation (ft)", value=68.76, step=0.01)
pvi_station = st.sidebar.number_input("PVI Station (ft)", value=1925.00, step=0.01)
pvi_elevation = st.sidebar.number_input("PVI Elevation (ft)", value=68.03, step=0.01)
g1 = st.sidebar.number_input("Initial Grade g₁ (%)", value=-2.0, step=0.01)
g2 = st.sidebar.number_input("Final Grade g₂ (%)", value=1.0, step=0.01)
station_input = st.sidebar.number_input("Enter Station to Evaluate (ft)", value=1958.63, step=0.01)

# --- Calculations ---
curve_length = abs(pvi_station - bvc_station) * 2
evc_station = bvc_station + curve_length
a_value = g2 - g1
g1_decimal = g1 / 100
station_within_limits = bvc_station <= station_input <= evc_station

# --- Calculate elevation at input station ---
elevation = None
if station_within_limits:
    x = station_input - bvc_station
    elevation = bvc_elevation + g1_decimal * x + (a_value / 100) * x**2 / (2 * curve_length)
    grade_at_x = g1
    st.markdown(f"**Elevation at station {station_input:.2f}:** {elevation:.4f} ft")
    st.markdown(f"**Grade at station {station_input:.2f}:** {grade_at_x:.4f} %")
else:
    st.warning("Station is outside the limits of the vertical curve.")

# --- Format station numbers like 1850.00 -> 18+50 ---
def station_format(station_val):
    return f"{int(station_val // 100)}+{int(station_val % 100):02d}"

# --- Profile Data ---
x_vals = np.arange(0, curve_length + 1, 1)
y_vals = bvc_elevation + g1_decimal * x_vals + (a_value / 100) * x_vals**2 / (2 * curve_length)

df = pd.DataFrame({
    "Station (ft)": x_vals + bvc_station,
    "Elevation (ft)": y_vals
})

evc_elevation = y_vals[-1]

# --- Label Points ---
label_df = pd.DataFrame({
    "Station (ft)": [
        bvc_station,
        pvi_station,
        evc_station,
        station_input if station_within_limits else np.nan
    ],
    "Elevation (ft)": [
        bvc_elevation,
        pvi_elevation,
        evc_elevation,
        elevation if station_within_limits else np.nan
    ],
    "Label": [
        f"BVC\n{station_format(bvc_station)}\nEL: {bvc_elevation:.2f}",
        f"PVI\n{station_format(pvi_station)}\nEL: {pvi_elevation:.2f}",
        f"EVC\n{station_format(evc_station)}\nEL: {evc_elevation:.2f}",
        f"Design Point\n{station_format(station_input)}\nEL: {elevation:.2f}" if station_within_limits else ""
    ]
}).dropna()

# --- Altair Chart ---
y_min = np.floor(min(y_vals)) - 1
y_max = np.ceil(max(y_vals)) + 1

curve = alt.Chart(df).mark_line(color="steelblue").encode(
    x=alt.X("Station (ft)", axis=alt.Axis(title="Station (ft)")),
    y=alt.Y("Elevation (ft)", scale=alt.Scale(domain=[y_min, y_max]),
            axis=alt.Axis(title="Elevation (ft)")),
    tooltip=["Station (ft)", "Elevation (ft)"]
)

points = alt.Chart(label_df).mark_point(color="red", size=70).encode(
    x="Station (ft)",
    y="Elevation (ft)",
    tooltip=["Label"]
)

text = alt.Chart(label_df).mark_text(
    align="left", baseline="middle", dx=5, dy=-10, fontSize=11, color="#D55E00"
).encode(
    x="Station (ft)",
    y="Elevation (ft)",
    text="Label"
)

st.subheader("Vertical Curve Profile")
st.altair_chart((curve + points + text).properties(width=700, height=400), use_container_width=True)