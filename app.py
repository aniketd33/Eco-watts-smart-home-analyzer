import streamlit as st
import pandas as pd
from charts import (
    plot_usage_by_appliance,
    plot_daily_cost_trend,
    plot_room_wise_usage,
)
import model  # ML forecast model

# ----------------------------
# 🌿 App Configuration
# ----------------------------
st.set_page_config(page_title="EcoWatts Smart Dashboard", page_icon="⚡", layout="wide")

# Inject custom CSS for styling
st.markdown("""
    <style>
    /* Global Styles */
    body { background-color: #f4f7f9; }
    .main { background-color: #ffffff; border-radius: 15px; padding: 25px; }
    h1, h2, h3 { color: #2b6777; }
    .stMetric { background: #eaf6f6; border-radius: 10px; padding: 10px; }
    .sidebar .sidebar-content { background-color: #2b6777; color: white; }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# Sidebar Navigation
# ----------------------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4151/4151388.png", width=80)
st.sidebar.title("⚡ EcoWatts Dashboard")
page = st.sidebar.radio("Navigate", [
    "📊 Overview Dashboard",
    "🔮 Energy Forecast",
    "🌱 Sustainability Insights"
])

st.sidebar.markdown("---")
st.sidebar.caption("Developed by Aniket Dombale | © 2025")

# ----------------------------
# Upload CSV Section
# ----------------------------
uploaded_file = st.sidebar.file_uploader("📤 Upload your energy dataset (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Normalize column names
    df.columns = [c.strip().replace(" ", "_") for c in df.columns]

    # Display data preview
    st.success("✅ Data uploaded successfully!")
    st.dataframe(df.head())

    # --------------------------------
    # PAGE 1: OVERVIEW DASHBOARD
    # --------------------------------
    if page == "📊 Overview Dashboard":
        st.title("📊 Smart Home Energy Overview")

        col1, col2 = st.columns(2)
        with col1:
            fig1 = plot_usage_by_appliance(df)
            st.pyplot(fig1)
        with col2:
            fig2 = plot_daily_cost_trend(df)
            st.pyplot(fig2)

        st.subheader("🏠 Room-wise Energy Usage")
        try:
            fig3 = plot_room_wise_usage(df)
            st.pyplot(fig3, use_container_width=True)
        except Exception as e:
            st.warning(f"⚠️ Unable to load Room-wise chart: {e}")

        st.info("""
        - This dashboard shows total and appliance-wise energy usage.
        - The daily trend helps you visualize cost patterns.
        - Room-wise charts highlight areas of high energy consumption.
        """)

    # --------------------------------
    # PAGE 2: ENERGY FORECAST
    # --------------------------------
    elif page == "🔮 Energy Forecast":
        st.title("🔮 Future Energy Usage Forecast")

        try:
            daily_data = model.prepare_forecast_data(df)
            trained_model, mae, r2 = model.train_forecast_model(daily_data)
            forecast_df = model.forecast_next_days(trained_model, daily_data)
            fig_forecast = model.plot_forecast_results(daily_data, forecast_df)

            st.plotly_chart(fig_forecast, use_container_width=True)
            st.success(f"✅ Model Performance: MAE = {mae:.2f}, R² = {r2:.2f}")

        except Exception as e:
            st.warning(f"⚠️ Forecasting unavailable: {e}")

    # --------------------------------
    # PAGE 3: SUSTAINABILITY INSIGHTS
    # --------------------------------
    elif page == "🌱 Sustainability Insights":
        st.title("🌱 EcoWatts Sustainability & Smart Alerts")

        # --- Carbon Footprint Calculation ---
        CO2_PER_KWH = 0.85  # kg CO₂ per kWh
        df['Carbon_Footprint_kg'] = df['Usage_kWh'] * CO2_PER_KWH
        total_co2 = df['Carbon_Footprint_kg'].sum()

        col1, col2, col3 = st.columns(3)
        col1.metric("🌍 Total Energy Used (kWh)", f"{df['Usage_kWh'].sum():.2f}")
        col2.metric("💰 Total Cost (INR)", f"{df['Cost(INR)'].sum():.2f}")
        col3.metric("♻️ Total Carbon Emission (kg CO₂)", f"{total_co2:.2f}")

        # --- Smart Alert Detection ---
        daily_usage = df.groupby(df['Timestamp'].dt.date)['Usage_kWh'].sum()
        mean_usage = daily_usage.mean()
        latest_usage = daily_usage.iloc[-1]

        if latest_usage > 1.5 * mean_usage:
            st.warning("⚠️ High energy usage detected today! Please check appliances.")
            alert_message = "Energy spike detected! Reduce unnecessary load."
        else:
            st.success("✅ Energy usage is normal.")
            alert_message = "All systems operating efficiently."

        # --- Eco-Tips Section ---
        st.markdown("### 💡 Eco-Friendly Tips")
        high_usage_appliance = df.groupby('Appliance')['Usage_kWh'].sum().idxmax()

        eco_tips = [
            f"Switch off your {high_usage_appliance} when not in use.",
            "Use LED bulbs instead of incandescent lights.",
            "Run washing machines and dishwashers in full loads.",
            "Maintain your air conditioner filters for better efficiency.",
            "Unplug idle devices to prevent phantom energy consumption."
        ]

        import random
        st.info(f"💚 Tip: {random.choice(eco_tips)}")

        # --- Carbon Emission by Appliance Chart ---
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(6, 4))
        df.groupby('Appliance')['Carbon_Footprint_kg'].sum().plot(kind='bar', color='#6a994e', ax=ax)
        ax.set_title("Appliance-wise Carbon Footprint")
        ax.set_ylabel("CO₂ Emission (kg)")
        st.pyplot(fig)

        st.caption("These insights promote sustainable habits and monitor environmental impact.")

else:
    st.warning("👆 Please upload a CSV file to start analysis.")

