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

        # Dynamic Y-axis range with 1-ft padding
        y_min = np.floor(min(y_vals)) - 1
        y_max = np.ceil(max(y_vals)) + 1
        y_range = [y_min, y_max]

        def format_station(station):
            ft = int(station)
            return f"{ft//100}+{ft%100:02d}"

        label_points = [
            ("BVC", bvc_station, bvc_elevation),
            ("PVI", pvi_station, pvi_elevation),
            ("Design Point", station_input, elevation),
            ("EVC", evc_station, evc_elevation)
        ]

        label_df = pd.DataFrame({
            "Station (ft)": [s for _, s, _ in label_points],
            "Elevation (ft)": [e for _, _, e in label_points],
            "Label": [
                f"{name}\n{format_station(station)}\n{elevation:.2f}"
                for name, station, elevation in label_points
            ]
        })

        line = alt.Chart(df).mark_line(interpolate='monotone', color="#0072B5").encode(
            x=alt.X("Station (ft)", axis=alt.Axis(title="Station (ft)")),
            y=alt.Y("Elevation (ft)", scale=alt.Scale(domain=y_range),
                    axis=alt.Axis(title="Elevation (ft)", tickMinStep=1)),
            tooltip=["Station (ft)", "Elevation (ft)"]
        )

        area = alt.Chart(df).mark_area(opacity=0.2, color="#0072B5").encode(
            x="Station (ft)",
            y=alt.Y("Elevation (ft)", scale=alt.Scale(domain=y_range),
                    axis=alt.Axis(tickMinStep=1))
        )

        points = alt.Chart(label_df).mark_point(filled=True, size=100).encode(
            x="Station (ft)",
            y="Elevation (ft)",
            color=alt.Color("Label", legend=None),
            tooltip=["Label", "Station (ft)", "Elevation (ft)"]
        )

        labels = alt.Chart(label_df).mark_text(
            align="left", baseline="middle", dx=5, dy=-10, color='white'
        ).encode(
            x="Station (ft)",
            y="Elevation (ft)",
            text="Label"
        )

        chart = (area + line + points + labels).properties(
            width=700,
            height=400,
            title="Vertical Curve Profile"
        ).interactive()

        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Please enter valid BVC and EVC stations to generate the graph.")