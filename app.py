import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
from charts import plot_usage_by_appliance, plot_daily_cost_trend, plot_room_wise_usage
import model
from fpdf import FPDF
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
    body { background-color: #f5f9f9; }
    .main { background-color: #ffffff; border-radius: 15px; padding: 25px; }
    h1, h2, h3 { color: #2b6777; }
    [data-testid="stSidebar"] {
        background-color: #2b6777;
        color: white;
    }
    [data-testid="stSidebar"] * {
        color: white;
    }
    .developer-info {
        position: fixed;
        bottom: 10px;
        left: 20px;
        color: white;
        font-size: 13px;
        opacity: 0.9;
    }
    .navbar {
        display: flex;
        justify-content: center;
        background-color: #2b6777;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    .nav-btn {
        background-color: #52b788;
        color: white;
        border: none;
        padding: 8px 16px;
        margin: 0 6px;
        border-radius: 6px;
        font-weight: 600;
        text-decoration: none;
        cursor: pointer;
    }
    .nav-btn:hover { background-color: #40916c; }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# 🏷️ App Title
# ------------------------------------------------
st.markdown("<h1 style='text-align:center;'>⚡ EcoWatts – Smart Home Energy Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align:center; color:#555;'>Real-Time Energy Insights • Forecasting • Sustainability</h5>", unsafe_allow_html=True)
st.markdown("---")

# ------------------------------------------------
# 📂 Auto-load Default Dataset + Optional Upload
# ------------------------------------------------
DEFAULT_PATH = "energy_usage_Dataset.csv"

try:
    df = pd.read_csv(DEFAULT_PATH)
    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df.columns = [c.strip().replace(" ", "_") for c in df.columns]
    st.info("📊 Demo dataset loaded automatically.")
except Exception as e:
    st.error(f"⚠️ Could not load demo dataset: {e}")
    df = pd.DataFrame()

uploaded_file = st.file_uploader("📤 Upload your own CSV file (optional)", type=["csv"])
if uploaded_file is not None:
    user_df = pd.read_csv(uploaded_file)
    if "Timestamp" in user_df.columns:
        user_df["Timestamp"] = pd.to_datetime(user_df["Timestamp"])
    user_df.columns = [c.strip().replace(" ", "_") for c in user_df.columns]
    df = user_df
    st.success("✅ Custom dataset uploaded successfully!")

if df.empty:
    st.warning("⚠️ No data available to display. Please upload a CSV file.")
    st.stop()

# ------------------------------------------------
# 🧭 Sidebar Filters
# ------------------------------------------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4151/4151388.png", width=80)
st.sidebar.title("⚡ EcoWatts Dashboard")

st.sidebar.markdown("### 🔍 Filter Energy Data")
selected_rooms = st.sidebar.multiselect("🏠 Select Room(s)", df["Room"].unique())
selected_appliances = st.sidebar.multiselect("🔌 Select Appliance(s)", df["Appliance"].unique())
date_range = st.sidebar.date_input("📅 Select Date Range", [])

if st.sidebar.button("🔁 Reset Filters"):
    st.session_state.clear()
    st.experimental_rerun()

st.sidebar.markdown("""
<div class="developer-info">
    <hr style='border: 1px solid #fff; opacity: 0.3;'>
    👨‍💻 <b>Developed by:</b> Aniket Dombale<br>© 2025 EcoWatts Project
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------
# 🔍 Apply Filters
# ------------------------------------------------
filtered_df = df.copy()
if selected_rooms:
    filtered_df = filtered_df[filtered_df["Room"].isin(selected_rooms)]
if selected_appliances:
    filtered_df = filtered_df[filtered_df["Appliance"].isin(selected_appliances)]
if date_range and len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df["Timestamp"].dt.date >= start_date)
        & (filtered_df["Timestamp"].dt.date <= end_date)
    ]

if filtered_df.empty:
    st.warning("⚠️ No records found for the selected filters.")
    st.stop()

# ------------------------------------------------
# 🌍 Dashboard Overview (Loads Immediately)
# ------------------------------------------------
st.markdown("### 🌍 Energy Summary Overview")
col1, col2, col3 = st.columns(3)
col1.metric("⚡ Total Energy (kWh)", f"{filtered_df['Usage_kWh'].sum():.2f}")
col2.metric("💰 Total Cost (INR)", f"{filtered_df['Cost(INR)'].sum():.2f}")
col3.metric("♻️ CO₂ Emission (kg)", f"{(filtered_df['Usage_kWh'].sum() * 0.85):.2f}")

# ------------------------------------------------
# 📊 Visual Insights (Uniform Chart Sizes)
# ------------------------------------------------
st.markdown("### 📈 Visual Insights")

c1, c2 = st.columns(2)
with c1:
    fig1 = plot_usage_by_appliance(filtered_df)
    fig1.set_size_inches(6, 4)
    st.pyplot(fig1)
with c2:
    fig2 = plot_daily_cost_trend(filtered_df)
    fig2.set_size_inches(6, 4)
    st.pyplot(fig2)

st.subheader("🏠 Room-wise Energy Usage")
fig3 = plot_room_wise_usage(filtered_df)
fig3.set_size_inches(6, 4)
st.pyplot(fig3)

# ------------------------------------------------
# 🔮 Energy Forecast
# ------------------------------------------------
st.markdown("### 🔮 Future Energy Usage Forecast")
daily_data = model.prepare_forecast_data(filtered_df)
trained_model, mae, r2 = model.train_forecast_model(daily_data)
forecast_df = model.forecast_next_days(trained_model, daily_data)
fig_forecast = model.plot_forecast_results(daily_data, forecast_df)
st.plotly_chart(fig_forecast, use_container_width=True)
st.info(f"✅ Forecast Model Performance: MAE = {mae:.2f}, R² = {r2:.2f}")

# ------------------------------------------------
# 🌱 Sustainability Section
# ------------------------------------------------
st.markdown("### 🌱 Smart Sustainability Insights")
CO2_PER_KWH = 0.85
filtered_df["Carbon_Footprint_kg"] = filtered_df["Usage_kWh"] * CO2_PER_KWH
total_co2 = filtered_df["Carbon_Footprint_kg"].sum()
col1, col2 = st.columns(2)
col1.metric("♻️ Total Carbon Emission", f"{total_co2:.2f} kg CO₂")
col2.info(f"💚 Tip: {random.choice(['Switch off unused appliances.', 'Use LED bulbs.', 'Unplug idle devices.', 'Clean AC filters.'])}")

# ------------------------------------------------
# 📑 Reports Section (Bottom)
# ------------------------------------------------
st.markdown("---")
st.markdown("<h4 style='text-align:center;'>📑 Reports & Export</h4>", unsafe_allow_html=True)
csv = filtered_df.to_csv(index=False).encode("utf-8")
col1, col2 = st.columns(2)
with col1:
    st.download_button("⬇️ Download Filtered Data (CSV)", csv, "EcoWatts_Report.csv", "text/csv", use_container_width=True)
with col2:
    if st.button("🖨️ Generate PDF Report", use_container_width=True):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, txt="EcoWatts – Smart Home Energy Analyzer", ln=True, align="C")
        pdf.set_font("Arial", "", 12)
        pdf.cell(200, 10, txt="Developed by: Aniket Dombale", ln=True, align="C")
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Total Energy: {filtered_df['Usage_kWh'].sum():.2f} kWh", ln=True)
        pdf.cell(200, 10, txt=f"Total Cost: {filtered_df['Cost(INR)'].sum():.2f} INR", ln=True)
        pdf.cell(200, 10, txt=f"CO₂ Emission: {total_co2:.2f} kg", ln=True)
        temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdf.output(temp_pdf.name)
        with open(temp_pdf.name, "rb") as file:
            st.download_button("⬇️ Download PDF Report", data=file, file_name="EcoWatts_Report.pdf", mime="application/pdf", use_container_width=True)
