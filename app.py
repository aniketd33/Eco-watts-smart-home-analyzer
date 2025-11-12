import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
from charts import (
    plot_usage_by_appliance,
    plot_daily_cost_trend,
    plot_room_wise_usage,
)
import model  # ML forecast model

# ----------------------------
# 🌿 App Configuration
# ----------------------------
st.set_page_config(page_title="EcoWatts – Smart Home Energy Analyzer", page_icon="⚡", layout="wide")

# ----------------------------
# 💅 Custom CSS Styling
# ----------------------------
st.markdown("""
    <style>
    body { background-color: #f4f7f9; }
    h1, h2, h3 { color: #2b6777; }
    [data-testid="stSidebar"] {
        background-color: #2b6777 !important;
        color: white !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    .developer-info {
        position: fixed;
        bottom: 10px;
        left: 20px;
        color: white;
        font-size: 13px;
        opacity: 0.9;
    }
    .upper-card {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# 🧭 Sidebar Navigation
# ----------------------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4151/4151388.png", width=80)
st.sidebar.title("⚡ EcoWatts – Smart Home Energy Analyzer")

page = st.sidebar.radio("Navigate", [
    "📊 Overview Dashboard",
    "🔮 Energy Forecast",
    "🌱 Sustainability Insights"
])

# Developer info fixed bottom
st.sidebar.markdown("""
    <div class="developer-info">
        <hr style="border: 1px solid #fff; opacity: 0.3;">
        👨‍💻 <b>Developed by:</b> Aniket Dombale<br>© 2025 EcoWatts Project
    </div>
""", unsafe_allow_html=True)

# ----------------------------
# 📤 Upload CSV Section
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

    # ----------------------------
    # 🔍 Data Filters + Reset Button
    # ----------------------------
    st.markdown("### 🔍 Filter Energy Data")

    rooms = df["Room"].unique().tolist() if "Room" in df.columns else []
    appliances = df["Appliance"].unique().tolist() if "Appliance" in df.columns else []
    min_date = df["Timestamp"].min().date()
    max_date = df["Timestamp"].max().date()

    # Create session state for reset
    if "reset" not in st.session_state:
        st.session_state.reset = False

    # Reset function
    def reset_filters():
        st.session_state.reset = True

    # Layout for filters + reset button
    col1, col2, col3, col4 = st.columns([1, 1, 1, 0.5])
    with col1:
        selected_rooms = st.multiselect("🏠 Select Room(s)", options=rooms, default=rooms if not st.session_state.reset else [])
    with col2:
        selected_appliances = st.multiselect("🔌 Select Appliance(s)", options=appliances, default=appliances if not st.session_state.reset else [])
    with col3:
        selected_dates = st.date_input("📅 Select Date Range", [min_date, max_date])
    with col4:
        st.write("")  # spacing
        if st.button("🔁 Reset Filters"):
            reset_filters()
            st.experimental_rerun()

    # Apply filters
    filtered_df = df.copy()
    if selected_rooms:
        filtered_df = filtered_df[filtered_df["Room"].isin(selected_rooms)]
    if selected_appliances:
        filtered_df = filtered_df[filtered_df["Appliance"].isin(selected_appliances)]
    if selected_dates and len(selected_dates) == 2:
        start_date, end_date = selected_dates
        filtered_df = filtered_df[(filtered_df["Timestamp"].dt.date >= start_date) &
                                  (filtered_df["Timestamp"].dt.date <= end_date)]

    st.success(f"✅ Showing {len(filtered_df)} records after applying filters.")

    # --------------------------------
    # PAGE 1: OVERVIEW DASHBOARD
    # --------------------------------
    if page == "📊 Overview Dashboard":
        st.title("📊 Smart Home Energy Overview")

        col1, col2 = st.columns(2)
        with col1:
            fig1 = plot_usage_by_appliance(filtered_df)
            st.pyplot(fig1)
        with col2:
            fig2 = plot_daily_cost_trend(filtered_df)
            st.pyplot(fig2)

        st.subheader("🏠 Room-wise Energy Usage")
        try:
            fig3 = plot_room_wise_usage(filtered_df)
            st.pyplot(fig3)
        except Exception as e:
            st.warning(f"⚠️ Unable to load Room-wise chart: {e}")

        st.info("""
        - The filters above update all charts instantly.  
        - Click **Reset Filters** 🔁 to show the complete dataset.  
        - View energy patterns by room, appliance, or date.
        """)

    # --------------------------------
    # PAGE 2: ENERGY FORECAST
    # --------------------------------
    elif page == "🔮 Energy Forecast":
        st.title("🔮 Energy Usage Forecast")

        try:
            daily_data = model.prepare_forecast_data(filtered_df)
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
        filtered_df['Carbon_Footprint_kg'] = filtered_df['Usage_kWh'] * CO2_PER_KWH
        total_co2 = filtered_df['Carbon_Footprint_kg'].sum()

        col1, col2, col3 = st.columns(3)
        col1.metric("🌍 Total Energy Used (kWh)", f"{filtered_df['Usage_kWh'].sum():.2f}")
        col2.metric("💰 Total Cost (INR)", f"{filtered_df['Cost(INR)'].sum():.2f}")
        col3.metric("♻️ Total Carbon Emission (kg CO₂)", f"{total_co2:.2f}")

        daily_usage = filtered_df.groupby(filtered_df['Timestamp'].dt.date)['Usage_kWh'].sum()
        mean_usage = daily_usage.mean()
        latest_usage = daily_usage.iloc[-1]

        if latest_usage > 1.5 * mean_usage:
            st.warning("⚠️ High energy usage detected today! Please check appliances.")
        else:
            st.success("✅ Energy usage is normal.")

        st.markdown("### 💡 Eco-Friendly Tips")
        high_usage_appliance = filtered_df.groupby('Appliance')['Usage_kWh'].sum().idxmax()
        eco_tips = [
            f"Switch off your {high_usage_appliance} when not in use.",
            "Use LED bulbs instead of incandescent lights.",
            "Run washing machines and dishwashers in full loads.",
            "Maintain your air conditioner filters for better efficiency.",
            "Unplug idle devices to prevent phantom energy consumption."
        ]
        st.info(f"💚 Tip: {random.choice(eco_tips)}")

        fig, ax = plt.subplots(figsize=(4, 3))
        filtered_df.groupby('Appliance')['Carbon_Footprint_kg'].sum().plot(kind='bar', color='#6a994e', ax=ax)
        ax.set_title("Appliance-wise Carbon Footprint")
        ax.set_ylabel("CO₂ Emission (kg)")
        st.pyplot(fig)

else:
    st.warning("👆 Please upload a CSV file to start analysis.")


