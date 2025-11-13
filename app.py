import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt

# Import functions from charts.py and model.py
from charts import (
    plot_usage_by_appliance,
    plot_daily_cost_trend,
    plot_room_wise_usage
)
import model


# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(page_title="EcoWatts – Smart Home Energy Analyzer", page_icon="⚡", layout="wide")


# ------------------------------------------------
# LOAD CUSTOM CSS
# ------------------------------------------------
try:
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("⚠ style.css not found. Using default theme.")


# ------------------------------------------------
# SIDEBAR TITLE (ALWAYS VISIBLE)
# ------------------------------------------------
st.sidebar.markdown(
    """
    <h2 style='color:white; text-align:center; font-size:25px;'>
        ⚡ EcoWatts Dashboard
    </h2>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------
# SIDEBAR NAVIGATION
# ------------------------------------------------
page = st.sidebar.radio(
    "Navigation Menu",
    ["Dashboard", "Forecast", "Sustainability", "Filters"]
)


# ------------------------------------------------
# LOAD DATA (AUTO + OPTIONAL UPLOAD)
# ------------------------------------------------
DEFAULT_PATH = "energy_usage_Dataset.csv"

try:
    df = pd.read_csv(DEFAULT_PATH)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df.columns = [c.strip().replace(" ", "_") for c in df.columns]
    st.info("📊 Demo dataset loaded automatically.")
except Exception:
    st.error("⚠ Could not load demo dataset.")
    df = pd.DataFrame()

uploaded_file = st.file_uploader("📤 Upload your dataset (optional)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df.columns = [c.strip().replace(" ", "_") for c in df.columns]
    st.success("✅ Custom Dataset Loaded!")


# ------------------------------------------------
# PAGE: DASHBOARD
# ------------------------------------------------
if page == "Dashboard":
    st.title("📊 EcoWatts – Smart Home Energy Analyzer")

    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    st.markdown("### 📈 Visual Analytics")

    col1, col2 = st.columns(2)

    with col1:
        fig1 = plot_usage_by_appliance(df)
        fig1.set_size_inches(6, 4)
        st.pyplot(fig1)

    with col2:
        fig2 = plot_daily_cost_trend(df)
        fig2.set_size_inches(6, 4)
        st.pyplot(fig2)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("🏠 Room-wise Usage")
        fig3 = plot_room_wise_usage(df)
        fig3.set_size_inches(6, 4)
        st.pyplot(fig3)

    with col4:
        st.info("📌 Add more visuals in this area if needed.")


# ------------------------------------------------
# PAGE: FORECAST
# ------------------------------------------------
elif page == "Forecast":
    st.title("🔮 Energy Usage Prediction")

    try:
        daily_data = model.prepare_forecast_data(df)
        trained_model, mae, r2 = model.train_forecast_model(daily_data)
        forecast_df = model.forecast_next_days(trained_model, daily_data)
        fig_forecast = model.plot_forecast_results(daily_data, forecast_df)

        st.plotly_chart(fig_forecast, use_container_width=True)

        st.success(f"📌 MAE: {mae:.2f} | R² Score: {r2:.2f}")

    except Exception as e:
        st.error(f"⚠ Forecasting Error: {e}")


# ------------------------------------------------
# PAGE: SUSTAINABILITY
# ------------------------------------------------
elif page == "Sustainability":
    st.title("🌱 Sustainability Insights")

    CO2_FACTOR = 0.85
    df["Carbon"] = df["Usage_kWh"] * CO2_FACTOR

    colA, colB, colC = st.columns(3)
    colA.metric("⚡ Total Energy (kWh)", f"{df['Usage_kWh'].sum():.2f}")
    colB.metric("💰 Total Cost (INR)", f"{df['Cost(INR)'].sum():.2f}")
    colC.metric("🌍 Carbon Emission (kg CO₂)", f"{df['Carbon'].sum():.2f}")

    st.subheader("⚠ Smart Alert System")
    daily_usage = df.groupby(df["Timestamp"].dt.date)["Usage_kWh"].sum()
    if daily_usage.iloc[-1] > 1.5 * daily_usage.mean():
        st.warning("⚡ High Usage Detected Today!")
    else:
        st.success("✅ Energy Levels Normal")

    st.subheader("💡 Eco-Friendly Tips")
    tips = [
        "Use LED bulbs instead of traditional bulbs.",
        "Turn off appliances when not in use.",
        "Clean AC filters regularly for better efficiency.",
        "Use natural ventilation during mornings.",
    ]
    st.info(random.choice(tips))


# ------------------------------------------------
# PAGE: FILTERS
# ------------------------------------------------
elif page == "Filters":
    st.title("🔍 Filter Energy Data")

    rooms = st.multiselect("Select Room(s)", options=df["Room"].unique())
    appliances = st.multiselect("Select Appliance(s)", options=df["Appliance"].unique())
    date_range = st.date_input("Select Date Range", [])

    df_filtered = df.copy()

    if rooms:
        df_filtered = df_filtered[df_filtered["Room"].isin(rooms)]
    if appliances:
        df_filtered = df_filtered[df_filtered["Appliance"].isin(appliances)]
    if len(date_range) == 2:
        start, end = date_range
        df_filtered = df_filtered[
            (df_filtered["Timestamp"].dt.date >= start) &
            (df_filtered["Timestamp"].dt.date <= end)
        ]

    st.dataframe(df_filtered)

    if st.button("Reset Filters"):
        st.experimental_rerun()


# ------------------------------------------------
# FOOTER
# ------------------------------------------------
st.markdown("---")
st.caption("Developed by **Aniket Dombale** | © 2025 EcoWatts Project")
