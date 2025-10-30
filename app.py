import streamlit as st
import pandas as pd
from charts import (
    plot_usage_by_appliance,
    plot_daily_cost_trend,
    plot_room_wise_usage
)
import model  # import your model.py

# ----------------------------
# 🌿 Smart Home Energy Analyzer
# ----------------------------
st.set_page_config(page_title="EcoWatts Dashboard", page_icon="⚡", layout="wide")

# ----------------------------
# 💅 Custom CSS Styling
# ----------------------------
st.markdown("""
<style>
/* Background & Font */
body {
    background-color: #f4f9f4;
    color: #1b4332;
    font-family: 'Poppins', sans-serif;
}

/* Main container */
.main {
    background-color: #ffffff;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(0, 128, 96, 0.15);
}

/* Header */
h1 {
    color: #2d6a4f !important;
    text-align: center;
    font-weight: 700 !important;
}

/* Subheaders */
h2, h3 {
    color: #40916c !important;
    border-left: 6px solid #74c69d;
    padding-left: 10px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #e9f5ec;
    border-right: 2px solid #74c69d;
}

button[kind="primary"] {
    background-color: #2d6a4f !important;
    color: white !important;
    border-radius: 8px !important;
}

/* Footer */
footer {
    text-align: center;
    color: #6c757d;
    padding: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Dashboard Title
# ----------------------------
st.title("⚡ Smart Home Energy Analyzer Dashboard")
st.markdown("""
Welcome to the **EcoWatts Dashboard** — your personal smart home energy analyzer.  
Gain insights into daily electricity usage, cost trends, and room-wise consumption.
""")

# ----------------------------
# Upload CSV Section
# ----------------------------
uploaded_file = st.file_uploader("📤 Upload your energy usage CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Convert Timestamp column
    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    st.success("✅ Data uploaded successfully!")
    st.dataframe(df.head())

    # ----------------------------
    # Charts Section
    # ----------------------------
    st.subheader("📊 Visual Insights")
    col1, col2 = st.columns(2)

    with col1:
        fig1 = plot_usage_by_appliance(df)
        st.pyplot(fig1)

    with col2:
        fig2 = plot_daily_cost_trend(df)
        st.pyplot(fig2)

    # ----------------------------
    # Room-wise Usage
    # ----------------------------
    st.subheader("🏠 Room-wise Energy Usage")
    try:
        fig3 = plot_room_wise_usage(df)
        st.pyplot(fig3, use_container_width=True)
    except Exception as e:
        st.warning(f"⚠️ Unable to load Room-wise chart: {e}")

    # ----------------------------
    # 🔮 Energy Forecast Section
    # ----------------------------
    st.header("🔮 Energy Usage Forecast")

    try:
        daily_data = model.prepare_forecast_data(df)
        trained_model, mae, r2 = model.train_forecast_model(daily_data)
        forecast_df = model.forecast_next_days(trained_model, daily_data)
        fig_forecast = model.plot_forecast_results(daily_data, forecast_df)

        st.plotly_chart(fig_forecast, use_container_width=True)
        st.info(f"✅ Model Performance: MAE = {mae:.2f}, R² = {r2:.2f}")

    except Exception as e:
        st.warning(f"⚠️ Forecasting unavailable: {e}")

    # ----------------------------
    # Insights Section
    # ----------------------------
    st.markdown("### 💡 Insights Summary")
    st.info("""
    - High consumption appliances indicate where to optimize energy use.  
    - The **Daily Cost Trend** helps track monthly electricity expenses.  
    - The **Room-wise Usage** chart highlights high-demand areas in the home.  
    - The **Forecasting** feature predicts future usage to plan consumption smartly.  
    - Data can be used for **IoT-based automation** and sustainability tracking.
    """)

else:
    st.warning("👆 Please upload a CSV file to begin analysis.")

# -----------------------------------------------------------
# Footer
# -----------------------------------------------------------
st.markdown('---')
st.markdown('<footer>👨‍💻 Developed by <b>Aniket Dombale</b> | © 2025 EcoWatts Project</footer>', unsafe_allow_html=True)
