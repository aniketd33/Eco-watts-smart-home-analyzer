import streamlit as st
import pandas as pd
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from charts import (
    plot_usage_by_appliance,
    plot_daily_cost_trend,
    plot_room_wise_usage,
    plot_peak_usage_timeline,
)
import model

# ---------------------------------------------------------
# 🌿 PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="EcoWatts Smart Home Energy Analyzer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 🌈 CUSTOM STYLING (CSS)
# ---------------------------------------------------------
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 🧭 SIDEBAR NAVIGATION
# ---------------------------------------------------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4814/4814268.png", width=100)
st.sidebar.title("⚡ EcoWatts Dashboard")
page = st.sidebar.radio(
    "Navigate to:",
    ["🏠 Overview", "📊 Insights", "🔮 Forecasting", "ℹ️ About"]
)
st.sidebar.markdown("---")
st.sidebar.markdown("**👨‍💻 Author:** Aniket Dombale\n© 2025 | Open Source Project")

# ---------------------------------------------------------
# 🏠 PAGE 1: OVERVIEW
# ---------------------------------------------------------
if page == "🏠 Overview":
    st.title("⚡ EcoWatts Smart Home Energy Analyzer")
    st.markdown("""
    Welcome to the **EcoWatts Dashboard** — your intelligent home energy analyzer.  
    Upload your dataset to visualize appliance usage, daily costs, and forecast energy needs.
    """)

    uploaded_file = st.file_uploader("📤 Upload your energy usage CSV file", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        # Convert Timestamp column
        if 'Timestamp' in df.columns:
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])

        st.success("✅ Data uploaded successfully!")
        st.dataframe(df.head())

        st.markdown("### 📈 Quick Metrics")
        total_usage = df['Usage_kWh'].sum()
        total_cost = df['Cost(INR)'].sum()
        avg_temp = df['Temp(C)'].mean()

        c1, c2, c3 = st.columns(3)
        c1.metric("🔋 Total Usage (kWh)", f"{total_usage:.2f}")
        c2.metric("💰 Total Cost (₹)", f"{total_cost:.2f}")
        c3.metric("🌡️ Avg Temperature (°C)", f"{avg_temp:.1f}")

# ---------------------------------------------------------
# 📊 PAGE 2: VISUAL INSIGHTS
# ---------------------------------------------------------
elif page == "📊 Insights":
    st.title("📊 Visual Insights Dashboard")

    uploaded_file = st.file_uploader("📤 Upload your energy usage CSV file", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if 'Timestamp' in df.columns:
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])

        col1, col2 = st.columns(2)
        with col1:
            fig1 = plot_usage_by_appliance(df)
            st.pyplot(fig1)
        with col2:
            fig2 = plot_daily_cost_trend(df)
            st.pyplot(fig2)

        st.markdown("---")
        st.subheader("🏠 Room-wise Energy Usage")
        fig3 = plot_room_wise_usage(df)
        st.pyplot(fig3)

        st.markdown("---")
        st.subheader("⏰ Peak Usage Timeline")
        fig4 = plot_peak_usage_timeline(df)
        st.pyplot(fig4)

    else:
        st.warning("👆 Please upload a CSV file to view insights.")

# ---------------------------------------------------------
# 🔮 PAGE 3: FORECASTING
# ---------------------------------------------------------
elif page == "🔮 Forecasting":
    st.title("🔮 Energy Usage Forecasting")

    uploaded_file = st.file_uploader("📤 Upload your dataset for forecasting", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if 'Timestamp' in df.columns:
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])

        try:
            daily_data = model.prepare_forecast_data(df)
            trained_model, mae, r2 = model.train_forecast_model(daily_data)
            forecast_df = model.forecast_next_days(trained_model, daily_data)
            fig_forecast = model.plot_forecast_results(daily_data, forecast_df)

            st.plotly_chart(fig_forecast, use_container_width=True)
            st.success(f"✅ Model Performance: MAE = {mae:.2f}, R² = {r2:.2f}")
        except Exception as e:
            st.warning(f"⚠️ Forecasting unavailable: {e}")
    else:
        st.info("📥 Upload a dataset to generate forecasts.")

# ---------------------------------------------------------
# ℹ️ PAGE 4: ABOUT
# ---------------------------------------------------------
elif page == "ℹ️ About":
    st.title("ℹ️ About EcoWatts Dashboard")
    st.markdown("""
    **EcoWatts** is a Streamlit-powered intelligent dashboard that visualizes and predicts
    household energy usage using **machine learning** and **data visualization**.

    **Key Features:**
    - Appliance-wise energy breakdown  
    - Daily cost trend visualization  
    - Room-wise power analytics  
    - ML-based forecasting of upcoming energy demand  

    **Developed by:** *Aniket Dombale*  
    **University:** Savitribai Phule Pune University  
    **Department:** Data Science (Department of Technology)
    """)

