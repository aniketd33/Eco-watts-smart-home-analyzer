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
from fpdf import FPDF  # For PDF generation
import tempfile

# ------------------------------------------------
# 🌿 App Configuration
# ------------------------------------------------
st.set_page_config(page_title="EcoWatts – Smart Home Energy Analyzer", page_icon="⚡", layout="wide")

# ------------------------------------------------
# 💅 Custom CSS Styling
# ------------------------------------------------
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
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# 🏷️ Main Title
# ------------------------------------------------
st.title("⚡ EcoWatts – Smart Home Energy Analyzer")
st.markdown("#### A Smart Energy Monitoring & Forecasting Dashboard")
st.markdown("---")

# ------------------------------------------------
# 📤 CSV Upload
# ------------------------------------------------
st.subheader("📤 Upload Your Energy Dataset (CSV)")
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"], key="main_upload")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Convert timestamp column if exists
    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df.columns = [c.strip().replace(" ", "_") for c in df.columns]

    # ------------------------------------------------
    # 🧭 Sidebar Filters
    # ------------------------------------------------
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4151/4151388.png", width=80)
    st.sidebar.title("⚡ EcoWatts Dashboard")
    st.sidebar.markdown("### 🔍 Filter Energy Data")

    # Appliance Filter
    if "Appliance" in df.columns:
        appliances = df["Appliance"].unique().tolist()
        selected_appliances = st.sidebar.multiselect("🔌 Select Appliance(s)", options=appliances, default=appliances)
    else:
        selected_appliances = []

    # Room Filter
    if "Room" in df.columns:
        rooms = df["Room"].unique().tolist()
        selected_rooms = st.sidebar.multiselect("🏠 Select Room(s)", options=rooms, default=rooms)
    else:
        selected_rooms = []

    # Date Range Filter
    if "Timestamp" in df.columns:
        min_date = df["Timestamp"].min().date()
        max_date = df["Timestamp"].max().date()
        selected_dates = st.sidebar.date_input("📅 Select Date Range", [min_date, max_date])
    else:
        selected_dates = None

    # Reset Filters Button
    st.sidebar.markdown("---")
    if st.sidebar.button("🔁 Reset Filters"):
        st.session_state.clear()
        st.experimental_rerun()

    # Sidebar Footer
    st.sidebar.markdown("""
        <div class="developer-info">
            <hr style='border: 1px solid #fff; opacity: 0.3;'>
            👨‍💻 <b>Developed by:</b> Aniket Dombale<br>© 2025 EcoWatts Project
        </div>
    """, unsafe_allow_html=True)

    # ------------------------------------------------
    # 📈 Apply Filters
    # ------------------------------------------------
    filtered_df = df.copy()
    if selected_rooms:
        filtered_df = filtered_df[filtered_df["Room"].isin(selected_rooms)]
    if selected_appliances:
        filtered_df = filtered_df[filtered_df["Appliance"].isin(selected_appliances)]
    if selected_dates and len(selected_dates) == 2:
        start_date, end_date = selected_dates
        filtered_df = filtered_df[
            (filtered_df["Timestamp"].dt.date >= start_date) &
            (filtered_df["Timestamp"].dt.date <= end_date)
        ]

    st.success(f"✅ Showing {len(filtered_df)} records after applying filters.")
    st.dataframe(filtered_df.head())

    # ------------------------------------------------
    # 📊 Dynamic Visuals
    # ------------------------------------------------
    st.markdown("### 📊 Energy Usage Insights")

    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(plot_usage_by_appliance(filtered_df))
    with col2:
        st.pyplot(plot_daily_cost_trend(filtered_df))

    st.subheader("🏠 Room-wise Energy Usage")
    try:
        st.pyplot(plot_room_wise_usage(filtered_df))
    except Exception as e:
        st.warning(f"⚠️ Unable to load Room-wise chart: {e}")

    # ------------------------------------------------
    # 🔮 Forecast Section
    # ------------------------------------------------
    st.markdown("---")
    st.header("🔮 Energy Usage Forecast")
    try:
        daily_data = model.prepare_forecast_data(filtered_df)
        trained_model, mae, r2 = model.train_forecast_model(daily_data)
        forecast_df = model.forecast_next_days(trained_model, daily_data)
        fig_forecast = model.plot_forecast_results(daily_data, forecast_df)
        st.plotly_chart(fig_forecast, use_container_width=True)
        st.success(f"✅ Model Performance: MAE = {mae:.2f}, R² = {r2:.2f}")
    except Exception as e:
        st.warning(f"⚠️ Forecasting unavailable: {e}")

    # ------------------------------------------------
    # 🌱 Sustainability (CO₂ Tracking, Alerts, Tips)
    # ------------------------------------------------
    st.markdown("---")
    st.header("🌱 Sustainability & Smart Alerts")

    if "Usage_kWh" in filtered_df.columns:
        CO2_PER_KWH = 0.85
        filtered_df["Carbon_Footprint_kg"] = filtered_df["Usage_kWh"] * CO2_PER_KWH
        total_co2 = filtered_df["Carbon_Footprint_kg"].sum()

        col1, col2, col3 = st.columns(3)
        col1.metric("🌍 Total Energy Used (kWh)", f"{filtered_df['Usage_kWh'].sum():.2f}")
        col2.metric("💰 Total Cost (INR)", f"{filtered_df['Cost(INR)'].sum():.2f}")
        col3.metric("♻️ Total Carbon Emission (kg CO₂)", f"{total_co2:.2f}")

        # Alerts
        daily_usage = filtered_df.groupby(filtered_df['Timestamp'].dt.date)['Usage_kWh'].sum()
        if len(daily_usage) > 0:
            mean_usage = daily_usage.mean()
            latest_usage = daily_usage.iloc[-1]
            if latest_usage > 1.5 * mean_usage:
                st.warning("⚠️ High energy usage detected today! Please check appliances.")
            else:
                st.success("✅ Energy usage is normal.")

        # Eco Tips
        st.markdown("### 💡 Eco-Friendly Tips")
        if "Appliance" in filtered_df.columns:
            high_usage_appliance = filtered_df.groupby('Appliance')['Usage_kWh'].sum().idxmax()
            eco_tips = [
                f"Switch off your {high_usage_appliance} when not in use.",
                "Use LED bulbs instead of incandescent lights.",
                "Run washing machines and dishwashers in full loads.",
                "Maintain your air conditioner filters for better efficiency.",
                "Unplug idle devices to prevent phantom energy consumption."
            ]
            tip = random.choice(eco_tips)
            st.info(f"💚 Tip: {tip}")

        # Carbon Chart
        fig, ax = plt.subplots(figsize=(4, 3))
        filtered_df.groupby('Appliance')['Carbon_Footprint_kg'].sum().plot(kind='bar', color='#6a994e', ax=ax)
        ax.set_title("Appliance-wise Carbon Footprint")
        ax.set_ylabel("CO₂ Emission (kg)")
        st.pyplot(fig)

    # ------------------------------------------------
    # 💾 Download Filtered Report (CSV)
    # ------------------------------------------------
    st.markdown("---")
    st.header("💾 Download Filtered Report")

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv,
        file_name="EcoWatts_Filtered_Report.csv",
        mime="text/csv"
    )

    # ------------------------------------------------
    # 🧾 Generate PDF Report
    # ------------------------------------------------
    st.markdown("---")
    st.header("📑 Generate PDF Report")

    if st.button("🖨️ Generate PDF Report"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, txt="EcoWatts – Smart Home Energy Analyzer", ln=True, align="C")

        pdf.set_font("Arial", "", 12)
        pdf.cell(200, 10, txt=f"Developed by: Aniket Dombale", ln=True, align="C")
        pdf.ln(10)

        pdf.multi_cell(0, 10, f"📅 Filter Range: {selected_dates[0]} to {selected_dates[1]}")
        pdf.multi_cell(0, 10, f"🏠 Rooms: {', '.join(selected_rooms) if selected_rooms else 'All'}")
        pdf.multi_cell(0, 10, f"🔌 Appliances: {', '.join(selected_appliances) if selected_appliances else 'All'}")
        pdf.ln(10)

        pdf.cell(200, 10, txt=f"🌍 Total Energy Used: {filtered_df['Usage_kWh'].sum():.2f} kWh", ln=True)
        pdf.cell(200, 10, txt=f"💰 Total Cost: {filtered_df['Cost(INR)'].sum():.2f} INR", ln=True)
        pdf.cell(200, 10, txt=f"♻️ Total CO₂ Emission: {filtered_df['Carbon_Footprint_kg'].sum():.2f} kg", ln=True)
        pdf.ln(10)

        pdf.multi_cell(0, 10, f"💡 Eco Tip: {tip}")
        pdf.ln(20)

        pdf.cell(200, 10, txt="© 2025 EcoWatts Project – Developed by Aniket Dombale", ln=True, align="C")

        temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdf.output(temp_pdf.name)

        with open(temp_pdf.name, "rb") as file:
            st.download_button(
                label="⬇️ Download PDF Report",
                data=file,
                file_name="EcoWatts_Report.pdf",
                mime="application/pdf"
            )

        st.success("✅ PDF Report generated successfully!")

else:
    st.warning("👆 Please upload a CSV file to start analysis.")


