import streamlit as st
import pandas as pd
from charts import (
    plot_usage_by_appliance,
    plot_daily_cost_trend,
    plot_room_wise_usage,
)
import model  # ML forecast model
import random
import matplotlib.pyplot as plt

# ----------------------------
# 🌿 App Configuration
# ----------------------------
st.set_page_config(page_title="EcoWatts – Smart Home Energy Analyzer", page_icon="⚡", layout="wide")

# Inject custom CSS for styling and uniform chart sizes
st.markdown("""
    <style>
    /* Global Styles */
    body { background-color: #f4f7f9; }
    .main { background-color: #ffffff; border-radius: 15px; padding: 25px; }
    h1, h2, h3 { color: #2b6777; }
    .stMetric { background: #eaf6f6; border-radius: 10px; padding: 10px; }
    .sidebar .sidebar-content { background-color: #2b6777; color: white; }
    .chart-container {
        height: 400px;
        width: 100%;
    }
    .small-chart {
        height: 200px;
        width: 100%;
    }
    .upper-card {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .niche-card {
        background-color: #eaf6f6;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        border-left: 5px solid #2b6777;
    }
    /* Developer Section (Bottom Left Corner) */
    .developer-info {
        position: fixed;
        bottom: 10px;
        left: 15px;
        color: white;
        font-size: 14px;
        opacity: 0.9;
    }
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

# Developer info fixed at bottom-left corner
st.sidebar.markdown("""
    <div class="developer-info">
        <hr style="border: 1px solid #fff; opacity: 0.3;">
        <p>👨‍💻 Developed by <b>Aniket Dombale</b><br>© 2025</p>
    </div>
""", unsafe_allow_html=True)

# ----------------------------
# Upper Card for Upload CSV
# ----------------------------
st.markdown('<div class="upper-card">', unsafe_allow_html=True)
st.subheader("📤 Upload Your Energy Dataset (CSV)")
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"], key="main_upload")
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    df.columns = [c.strip().replace(" ", "_") for c in df.columns]

    st.success("✅ Data uploaded successfully!")
    st.dataframe(df.head())

    # --------------------------------
    # PAGE 1: OVERVIEW DASHBOARD
    # --------------------------------
    if page == "📊 Overview Dashboard":
        st.title("📊 Smart Home Energy Overview")

        st.header("Step-by-Step Guide to Using the Dashboard")
        st.markdown("""
        1. **Upload Data** using the upper card above.  
        2. **Explore Charts** for appliance, daily, and room trends.  
        3. **Check Insights** to optimize energy usage.  
        4. **Navigate** to Forecast or Sustainability tabs.
        """)

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
            st.subheader("🏠 Room-wise Energy Usage")
            try:
                fig3 = plot_room_wise_usage(df)
                fig3.set_size_inches(6, 4)
                st.pyplot(fig3)
            except Exception as e:
                st.warning(f"⚠️ Unable to load Room-wise chart: {e}")
        with col4:
            st.subheader("Additional Chart Placeholder")
            st.info("Add more charts here if needed.")

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

        CO2_PER_KWH = 0.85
        df['Carbon_Footprint_kg'] = df['Usage_kWh'] * CO2_PER_KWH
        total_co2 = df['Carbon_Footprint_kg'].sum()

        col1, col2, col3 = st.columns(3)
        col1.metric("🌍 Total Energy Used (kWh)", f"{df['Usage_kWh'].sum():.2f}")
        col2.metric("💰 Total Cost (INR)", f"{df['Cost(INR)'].sum():.2f}")
        col3.metric("♻️ Total Carbon Emission (kg CO₂)", f"{total_co2:.2f}")

        daily_usage = df.groupby(df['Timestamp'].dt.date)['Usage_kWh'].sum()
        mean_usage = daily_usage.mean()
        latest_usage = daily_usage.iloc[-1]

        if latest_usage > 1.5 * mean_usage:
            st.warning("⚠️ High energy usage detected today! Please check appliances.")
        else:
            st.success("✅ Energy usage is normal.")

        st.markdown("### 💡 Eco-Friendly Tips")
        high_usage_appliance = df.groupby('Appliance')['Usage_kWh'].sum().idxmax()
        eco_tips = [
            f"Switch off your {high_usage_appliance} when not in use.",
            "Use LED bulbs instead of incandescent lights.",
            "Run washing machines and dishwashers in full loads.",
            "Maintain your air conditioner filters for better efficiency.",
            "Unplug idle devices to prevent phantom energy consumption."
        ]
        st.info(f"💚 Tip: {random.choice(eco_tips)}")

        fig, ax = plt.subplots(figsize=(4, 3))
        df.groupby('Appliance')['Carbon_Footprint_kg'].sum().plot(kind='bar', color='#6a994e', ax=ax)
        ax.set_title("Appliance-wise Carbon Footprint")
        ax.set_ylabel("CO₂ Emission (kg)")
        st.pyplot(fig)

else:
    st.warning("👆 Please upload a CSV file to start analysis.")
