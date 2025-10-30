import streamlit as st
import pandas as pd
from charts import (
    plot_usage_by_appliance,
    plot_daily_cost_trend,
    plot_room_wise_usage
)
import model

# -----------------------------------------------------
# 🌿 App Configuration
# -----------------------------------------------------
st.set_page_config(
    page_title="EcoWatts Smart Energy Dashboard",
    page_icon="⚡",
    layout="wide"
)

# -----------------------------------------------------
# 🎨 Custom CSS for Modern UI
# -----------------------------------------------------
st.markdown("""
<style>
body {
    background-color: #f4f9f4;
    color: #1b4332;
    font-family: 'Poppins', sans-serif;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #d8f3dc 0%, #b7e4c7 100%);
}
h1, h2, h3 {
    color: #2d6a4f !important;
}
.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
}
div[data-testid="stMetricValue"] {
    color: #2d6a4f !important;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------
# 🧭 Sidebar Navigation
# -----------------------------------------------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/809/809957.png", width=80)
st.sidebar.title("⚡ EcoWatts Menu")

menu = st.sidebar.radio(
    "Navigate",
    ["📊 Dashboard", "🔍 Analytics", "🔮 Forecast", "ℹ️ About"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Developed by Aniket Dombale © 2025")

# -----------------------------------------------------
# 📂 Data Upload
# -----------------------------------------------------
uploaded_file = st.sidebar.file_uploader("Upload CSV Data", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
else:
    st.warning("👆 Please upload your dataset to continue.")
    st.stop()

# -----------------------------------------------------
# 📊 Dashboard Page
# -----------------------------------------------------
if menu == "📊 Dashboard":
    st.title("⚡ Smart Home Energy Dashboard")
    st.write("Visualize your energy usage, costs, and room-wise consumption at a glance.")

    st.metric("Total Energy Used (kWh)", f"{df['Usage_kWh'].sum():.2f}")
    st.metric("Total Cost (INR)", f"{df['Cost(INR)'].sum():.2f}")
    st.metric("Average Temperature (°C)", f"{df['Temp(C)'].mean():.1f}")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_usage_by_appliance(df), use_container_width=True)
    with col2:
        st.plotly_chart(plot_daily_cost_trend(df), use_container_width=True)

# -----------------------------------------------------
# 🔍 Analytics Page
# -----------------------------------------------------
elif menu == "🔍 Analytics":
    st.title("📊 In-depth Analytics")
    st.write("Explore detailed insights by room and appliance.")

    try:
        fig_room = plot_room_wise_usage(df)
        st.plotly_chart(fig_room, use_container_width=True)
    except Exception as e:
        st.warning(f"⚠️ Could not load chart: {e}")

    st.info("""
    💡 **Insights:**
    - Identify which rooms or appliances consume the most energy.
    - Use these insights to optimize your home’s efficiency.
    """)

# -----------------------------------------------------
# 🔮 Forecast Page
# -----------------------------------------------------
elif menu == "🔮 Forecast":
    st.title("🔮 Energy Usage Forecasting")
    st.write("Predict future energy consumption using regression-based modeling.")

    try:
        daily_data = model.prepare_forecast_data(df)
        trained_model, mae, r2 = model.train_forecast_model(daily_data)
        forecast_df = model.forecast_next_days(trained_model, daily_data)
        fig_forecast = model.plot_forecast_results(daily_data, forecast_df)

        st.plotly_chart(fig_forecast, use_container_width=True)
        st.success(f"✅ Model Performance: MAE = {mae:.2f}, R² = {r2:.2f}")
    except Exception as e:
        st.warning(f"⚠️ Forecasting unavailable: {e}")

# -----------------------------------------------------
# ℹ️ About Page
# -----------------------------------------------------
elif menu == "ℹ️ About":
    st.title("ℹ️ About EcoWatts")
    st.markdown("""
    **EcoWatts – Smart Home Energy Analyzer**  
    Built with ❤️ using **Streamlit**, **Plotly**, and **Scikit-learn**.

    This dashboard helps you:
    - Visualize energy consumption trends.
    - Detect high-usage appliances.
    - Predict future electricity demands.
    - Plan energy-saving strategies.

    ---
    👨‍💻 **Author:** Aniket Dombale  
    🏫 Savitribai Phule Pune University  
    📅 Year: 2025
    """)

    st.image("https://cdn-icons-png.flaticon.com/512/709/709699.png", width=100)

