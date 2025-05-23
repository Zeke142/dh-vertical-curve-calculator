import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
import altair as alt

st.set_page_config(page_title="DirtHub Tools: Vertical Curve Designer", layout="centered")

# Display logo
st.image("assets/dirthub_logo.png", width=250)
st.header("Vertical Curve Designer")
st.caption("“Engineered for real-world grading challenges.”")

# Input Mode Selection
input_mode = st.radio("Choose Input Method:", ("Elevation-Based", "Grade-Based"))

# Elevation-Based Input Mode
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
    curve_length = evc_station - bvc_station

    bvc_elevation = st.number_input("BVC Elevation", step=0.01)
    g1 = st.number_input("Grade In (g₁) [%]", step=0.01, format="%.2f")
    g2 = st.number_input("Grade Out (g₂) [%]", step=0.01, format="%.2f")
    pvi_station = (bvc_station + evc_station) / 2
    pvi_elevation = bvc_elevation + (g1 / 100) * (pvi_station - bvc_station)

# Common Calculations
a_value = g2 - g1

# Optional K-value
use_custom_k = st.checkbox("Enter custom K-value?")
if use_custom_k:
    k_value = st.number_input("K-value", step=0.01)
else:
    if a_value == 0 or curve_length == 0:
        k_value = "Undefined (check inputs)"
    else:
        k_value = curve_length / abs(a_value)

# Display Summary
st.header("Results")
st.markdown(f"**Curve Length (L):** {curve_length:.4f} ft")
st.markdown(f"**Grade In (g₁):** {g1:.4f} %")
st.markdown(f"**Grade Out (g₂):** {g2:.4f} %")
st.markdown(f"**A = g₂ - g₁:** {a_value:.4f} %")
st.markdown(f"**K-value:** {k_value if isinstance(k_value, str) else f'{k_value:.4f}'}")

# Elevation and Grade at Any Station
st.subheader("Elevation at Any Station")
station_input = st.number_input("Enter Station", step=1.0, format="%.2f")

if bvc_station <= station_input <= evc_station:
    x = station_input - bvc_station
    g1_decimal = g1 / 100

    if curve_length != 0:
        elevation = bvc_elevation + g1_decimal * x + (a_value / 100) * x**2 / (2 * curve_length)
        grade_at_x = g1 + (a_value * x / curve_length)
    else:
        elevation = bvc_elevation
        grade_at_x = g1

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

    y_min = np.floor(min(y_vals)) - 1
    y_max = np.ceil(max(y_vals)) + 1
    y_range = [y_min, y_max]

    def format_station(station):
        ft = int(station)
        return f"{ft//100}+{ft%100:02d}"

    label_points = [
        ("BVC", bvc_station, bvc_elevation),
        ("PVI", pvi_station, pvi_elevation),
        ("EVC", evc_station, evc_elevation)
    ]

    design_point = ("Design Point", station_input, elevation)

    base_labels = pd.DataFrame({
        "Name": [p[0] for p in label_points],
        "Station (ft)": [p[1] for p in label_points],
        "Elevation (ft)": [p[2] for p in label_points],
    })

    design_df = pd.DataFrame({
        "Name": [design_point[0]],
        "Station (ft)": [design_point[1]],
        "Elevation (ft)": [y_min + 1],  # offset for visibility
        "Actual Elevation": [design_point[2]]
    })

    # Layered text labels
    def create_label_layer(df, text_col, dy, color):
        return alt.Chart(df).mark_text(
            align="left", baseline="middle", dx=5, dy=dy, color=color, fontWeight='bold'
        ).encode(
            x="Station (ft)",
            y="Elevation (ft)",
            text=text_col
        )

    # Split label content
    base_labels["label_name"] = base_labels["Name"]
    base_labels["label_station"] = base_labels["Station (ft)"].apply(format_station)
    base_labels["label_elevation"] = base_labels["Elevation (ft)"].apply(lambda e: f"El: {e:.2f}")

    design_df["label_name"] = design_df["Name"]
    design_df["label_station"] = design_df["Station (ft)"].apply(format_station)
    design_df["label_elevation"] = design_df["Actual Elevation"].apply(lambda e: f"El: {e:.2f}")

    # Combine all text layers
    name_labels = create_label_layer(base_labels, "label_name", dy=-20, color="#7DC9FF")
    station_labels = create_label_layer(base_labels, "label_station", dy=-5, color="#FF6B00")
    elevation_labels = create_label_layer(base_labels, "label_elevation", dy=10, color="#FFFFFF")

    design_name = create_label_layer(design_df, "label_name", dy=-20, color="#7DC9FF")
    design_station = create_label_layer(design_df, "label_station", dy=-5, color="#FF6B00")
    design_elevation = create_label_layer(design_df, "label_elevation", dy=10, color="#FFFFFF")

    point_df = pd.concat([base_labels[["Station (ft)", "Elevation (ft)", "Name"]],
                          design_df[["Station (ft)", "Elevation (ft)", "Name"]]])
    points = alt.Chart(point_df).mark_point(filled=True, size=100).encode(
        x="Station (ft)",
        y="Elevation (ft)",
        color=alt.Color("Name", legend=None),
        tooltip=["Name", "Station (ft)", "Elevation (ft)"]
    )

    line = alt.Chart(df).mark_line(interpolate='monotone', color="#0072B5").encode(
        x="Station (ft)",
        y=alt.Y("Elevation (ft)", scale=alt.Scale(domain=y_range),
                axis=alt.Axis(title="Elevation (ft)", tickMinStep=1))
    )

    area = alt.Chart(df).mark_area(opacity=0.2, color="#0072B5").encode(
        x="Station (ft)",
        y=alt.Y("Elevation (ft)", scale=alt.Scale(domain=y_range))
    )

    chart = (area + line + points +
             name_labels + station_labels + elevation_labels +
             design_name + design_station + design_elevation
             ).properties(
        width=700,
        height=400,
        title="Vertical Curve Profile"
    ).interactive()

    st.altair_chart(chart, use_container_width=True)
else:
    st.info("Please enter valid BVC and EVC stations to generate the graph.")

# --- Email Capture ---
st.markdown("---")
st.subheader("Join the Beta List")
email = st.text_input("Enter your email to get updates and Pro access later")

if st.button("Join Waitlist"):
    if "@" in email and "." in email:
        with open("data/emails.txt", "a") as f:
            f.write(f"{email} - {datetime.now()}\n")
        st.success("You're on the list!")
    else:
        st.error("Please enter a valid email.")
