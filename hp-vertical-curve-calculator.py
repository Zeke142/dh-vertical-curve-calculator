import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title("Vertical Curve Calculator")

# --- Input Parameters ---
st.sidebar.header("Input Parameters")
bvc_station = st.sidebar.number_input("BVC Station (ft)", value=1850.00, step=0.01)
bvc_elevation = st.sidebar.number_input("BVC Elevation (ft)", value=68.76, step=0.01)
pvi_station = st.sidebar.number_input("PVI Station (ft)", value=1925.00, step=0.01)
pvi_elevation = st.sidebar.number_input("PVI Elevation (ft)", value=68.03, step=0.01)
g1 = st.sidebar.number_input("Initial Grade g1 (%)", value=-2.0, step=0.01)
g2 = st.sidebar.number_input("Final Grade g2 (%)", value=1.0, step=0.01)

curve_length = abs(pvi_station - bvc_station) * 2
a_value = g2 - g1
evc_station = bvc_station + curve_length
g1_decimal = g1 / 100

# --- Evaluate a Specific Station ---
station_input = st.number_input("Enter Station to Evaluate (ft)", value=1958.63, step=0.01)
station_within_limits = bvc_station <= station_input <= evc_station

if station_within_limits:
    x = station_input - bvc_station
    elevation = bvc_elevation + g1_decimal * x + (a_value / 100) * x**2 / (2 * curve_length)
    st.markdown(f"**Elevation at station {station_input:.2f}:** {elevation:.4f} ft")
    st.markdown(f"**Grade at station {station_input:.2f}:** {g1:.4f} %")
else:
    st.warning("Station is outside the limits of the vertical curve.")

# --- Helper for Station Format ---
def station_format(ft_val):
    return f"{int(ft_val // 100)}+{int(ft_val % 100):02d}"

# --- Vertical Curve Plot ---
st.subheader("Vertical Curve Profile")
if curve_length > 0:
    x_vals = np.arange(0, curve_length + 1, 1)
    y_vals = bvc_elevation + g1_decimal * x_vals + (a_value / 100) * x_vals**2 / (2 * curve_length)
    evc_elevation = y_vals[-1]

    df = pd.DataFrame({
        "Station (ft)": x_vals + bvc_station,
        "Elevation (ft)": y_vals
    })

    # Label points
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

    # Plot
    fig, ax = plt.subplots()
    ax.plot(df["Station (ft)"], df["Elevation (ft)"], color='blue', label="Vertical Curve")
    for _, row in label_df.iterrows():
        ax.plot(row["Station (ft)"], row["Elevation (ft)"], 'ro')
        ax.text(row["Station (ft)"], row["Elevation (ft)"] + 0.2, row["Label"],
                fontsize=8, ha='center', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=0.5))

    ax.set_xlabel("Station (ft)")
    ax.set_ylabel("Elevation (ft)")
    ax.set_title("Vertical Curve Profile")
    ax.grid(True)
    st.pyplot(fig)
else:
    st.warning("Curve length must be greater than zero to display the profile.")