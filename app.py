import streamlit as st
import pandas as pd
import plotly.express as px
import base64

from charts import (
    plot_usage_by_appliance,
    plot_daily_cost_trend,
    plot_room_wise_usage,
    plot_peak_usage_timeline,
)
import model  # ML forecasting

# -------------------------- PAGE CONFIG --------------------------------
st.set_page_config(page_title="EcoWatts – Smart Energy Analyzer", page_icon="⚡", layout="wide")

# -------------------------- CUSTOM CSS ---------------------------------
st.markdown("""
<style>
/* Background gradient */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(120deg, #e0f7fa, #e8f5e9);
    color: #0d1b2a;
}

/* Sidebar style */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #b2dfdb, #a5d6a7);
    color: #004d40;
}

/* Headers */
h1, h2, h3 {
    color: #004d40 !important;
    font-family: 'Poppins', sans-serif;
}

/* Buttons and inputs */
.stButton > button {
    background-color: #00796b;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 0.6em 1.2em;
    font-weight: 600;
}
.stButton > button:hover {
    background-color: #004d40;
}

/* Info boxes */
.stAlert {
    border-radius: 10px;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background-color: rgba(255,255,255,0.7);
    border-radius: 12px;
    padding: 1em;
}

/* Cards */
.block-container {
    padding-top: 2rem;
}

/* Footer */
.footer {
    text-align: center;
    padding: 1.5rem;
    font-size: 0.9rem;
    color: #004d40;
    opacity: 0.8;
}
</style>
""", unsafe_allow_html=True)

# -------------------------- SIDEBAR ---------------------------------
st.sidebar.title("⚡ EcoWatts Menu")
st.sidebar.markdown("### Navigate")
page = st.sidebar.radio("",
                        ["🏠 Dashboard", "📊 Analytics", "🔮 Forecast", "ℹ️ About"],
                        label_visibility="collapsed")

st.sidebar.markdown("---")
st.sidebar.info("Developed by **Aniket Dombale © 2025**")
uploaded_file = st.sidebar.file_uploader("Upload CSV Data", type=["csv"])

# -------------------------- MAIN DASHBOARD -----------------------------
st.title("⚡ EcoWatts – Smart Home Energy Analyzer")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    # Dashboard
    if page == "🏠 Dashboard":
        st.subheader("🏡 Overview Dashboard")

        total_usage = df["Usage_kWh"].sum()
        total_cost = df["Cost(INR)"].sum()
        avg_temp = df["Temp(C)"].mean()

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Energy Used (kWh)", f"{total_usage:.2f}")
        col2.metric("Total Cost (INR)", f"₹{total_cost:.2f}")
        col3.metric("Average Temperature (°C)", f"{avg_temp:.1f}")

        st.markdown("### ⚙️ Appliance-wise Usage")
        fig1 = plot_usage_by_appliance(df)
        st.plotly_chart(fig1, use_container_width=True)

        st.markdown("### 🕒 Peak Usage Timeline")
        fig4 = plot_peak_usage_timeline(df)
        st.plotly_chart(fig4, use_container_width=True)

    # Analytics
    elif page == "📊 Analytics":
        st.subheader("📈 Detailed Analytics")

        fig2 = plot_daily_cost_trend(df)
        st.plotly_chart(fig2, use_container_width=True)

        fig3 = plot_room_wise_usage(df)
        st.plotly_chart(fig3, use_container_width=True)

    # Forecast
    elif page == "🔮 Forecast":
        st.subheader("🔮 Energy Usage Forecast")

        try:
            daily_data = model.prepare_forecast_data(df)
            trained_model, mae, r2 = model.train_forecast_model(daily_data)
            forecast_df = model.forecast_next_days(trained_model, daily_data)
            fig_forecast = model.plot_forecast_results(daily_data, forecast_df)

            st.plotly_chart(fig_forecast, use_container_width=True)
            st.info(f"✅ Model Performance: MAE = {mae:.2f}, R² = {r2:.2f}")

        except Exception as e:
            st.warning(f"⚠️ Forecasting unavailable: {e}")

    # About
    else:
        st.subheader("ℹ️ About This Project")
        st.write("""
        EcoWatts is a smart analytics dashboard designed to help households monitor and optimize 
        their electricity usage efficiently.  
        **Features include:**
        - Appliance and room-level insights  
        - Daily and peak usage visualization  
        - AI-powered energy forecasting  
        - Clean, professional UI for easy interpretation
        """)

else:
    st.warning("👋 Please upload your dataset to continue.")

# -------------------------- FOOTER ---------------------------------
st.markdown("""
<div class="footer">
    © 2025 EcoWatts | Powered by Streamlit ⚡
</div>
""", unsafe_allow_html=True)

