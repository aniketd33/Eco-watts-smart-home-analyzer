import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import plotly.express as px

# ---------------------------------
# 🧠 App Title and Description
# ---------------------------------
st.set_page_config(page_title="EcoWatts – Smart Home Energy Analyzer", layout="wide")
st.title("⚡ EcoWatts – Smart Home Energy Analyzer 🌿")
st.markdown("""
EcoWatts helps you **analyze, forecast, and optimize** your home’s energy consumption.  
Upload your dataset and get smart insights about energy usage, cost, and efficiency.
""")

# ---------------------------------
# 📂 File Upload Section
# ---------------------------------
uploaded_file = st.file_uploader("📤 Upload your energy usage dataset (CSV format)", type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")
    
    # ---------------------------------
    # 🧹 Data Preview
    # ---------------------------------
    st.subheader("📊 Data Overview")
    st.dataframe(df.head())

    # Ensure timestamp is datetime
    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df['Date'] = df['Timestamp'].dt.date

    # ---------------------------------
    # 🔍 Basic Analytics
    # ---------------------------------
    st.subheader("📈 Energy Usage Summary")

    total_usage = df['Usage_kWh'].sum()
    total_cost = df['Cost(INR)'].sum()
    avg_temp = df['Temp(C)'].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Energy Used (kWh)", f"{total_usage:.2f}")
    col2.metric("Total Cost (INR)", f"{total_cost:.2f}")
    col3.metric("Average Temperature (°C)", f"{avg_temp:.1f}")

    # ---------------------------------
    # 🏠 Appliance-wise Usage
    # ---------------------------------
    if 'Appliance' in df.columns:
        st.subheader("🔌 Appliance-wise Energy Usage")
        appliance_usage = df.groupby('Appliance')['Usage_kWh'].sum().reset_index()
        fig1 = px.bar(appliance_usage, x='Appliance', y='Usage_kWh', color='Appliance',
                      title='Appliance-wise Total Energy Consumption')
        st.plotly_chart(fig1, use_container_width=True)

    # ---------------------------------
    # 📅 Daily Usage Aggregation
    # ---------------------------------
    daily_df = df.groupby('Date')['Usage_kWh'].sum().reset_index()
    daily_df['Day_Index'] = np.arange(len(daily_df))

    st.subheader("📅 Daily Energy Consumption Trend")
    fig2 = px.line(daily_df, x='Date', y='Usage_kWh', markers=True,
                   title='Daily Energy Usage Over Time')
    st.plotly_chart(fig2, use_container_width=True)

    # ---------------------------------
    # 🔮 Forecast Next 10 Days
    # ---------------------------------
    model = LinearRegression()
    X = daily_df[['Day_Index']]
    y = daily_df['Usage_kWh']
    model.fit(X, y)

    future_index = np.arange(len(daily_df), len(daily_df) + 10).reshape(-1, 1)
    future_usage = model.predict(future_index)
    future_dates = pd.date_range(start=daily_df['Date'].max() + pd.Timedelta(days=1), periods=10)
    future_df = pd.DataFrame({'Date': future_dates, 'Predicted_Usage_kWh': future_usage})

    st.subheader("🔮 Forecasted Energy Usage (Next 10 Days)")
    fig3 = px.line(future_df, x='Date', y='Predicted_Usage_kWh', markers=True,
                   title='Predicted Daily Energy Usage')
    st.plotly_chart(fig3, use_container_width=True)

    # ---------------------------------
    # 💰 Cost vs Usage
    # ---------------------------------
    st.subheader("💰 Energy Cost vs Usage")
    cost_usage = df.groupby('Date')[['Usage_kWh', 'Cost(INR)']].sum().reset_index()
    fig4 = px.scatter(cost_usage, x='Usage_kWh', y='Cost(INR)', size='Cost(INR)',
                      color='Usage_kWh', title='Cost vs Energy Usage')
    st.plotly_chart(fig4, use_container_width=True)

    # ---------------------------------
    # 🌱 Eco-Friendly Recommendations
    # ---------------------------------
    st.subheader("🌱 Smart Energy-Saving Recommendations")

    if total_usage > 200:
        st.info("💡 Tip: Your total usage is quite high. Try switching to energy-efficient appliances or reduce AC usage during peak hours.")
    if avg_temp > 27:
        st.info("🌡️ Tip: High temperature detected — consider using fans or natural ventilation before turning on air conditioners.")
    if 'Water Heater' in df['Appliance'].values:
        st.info("🚿 Tip: Use your water heater in Eco mode and during off-peak hours to reduce energy costs.")

    st.success("✅ Analysis Completed! Scroll up to view interactive graphs and insights.")

else:
    st.warning("📁 Please upload a dataset to begin the analysis.")
