⚡ EcoWatts – Smart Home Energy Analyzer 🌿

📘 Overview:
**EcoWatts** is a smart energy analytics system that monitors and analyzes home electricity consumption to promote **energy efficiency** and **cost savings**.  
It uses **IoT-inspired data**, **machine learning models**, and **interactive visualizations** to help users understand their energy usage patterns and plan for a more sustainable lifestyle.

🎯 Objectives:
- Analyze appliance-wise and room-wise energy consumption.  
- Predict future electricity usage using **Linear Regression**.  
- Visualize consumption trends and cost patterns interactively.  
- Provide eco-friendly recommendations for energy savings.

⚙️ Features:
✅ **Real-Time Monitoring** – Displays electricity usage per appliance and room.  
✅ **Forecasting** – Predicts future energy usage based on past data.  
✅ **Cost Analysis** – Calculates and visualizes daily/monthly cost patterns.  
✅ **Visualization Dashboard** – Built with Streamlit for easy data interaction.  
✅ **Eco-Tips** – Suggests optimal usage patterns for saving power and reducing bills.  

🧩 Tech Stack:

| Category | Tools / Libraries |
|-----------|-------------------|
| Programming | Python |
| Data Analysis | Pandas, NumPy |
| Machine Learning | Scikit-learn (Linear Regression) |
| Visualization | Matplotlib, Seaborn, Plotly |
| Web Framework | Streamlit |
| Dataset Format | CSV (IoT-based hourly data) |


🧠 Machine Learning Workflow:

1. **Data Collection** – Hourly appliance data from IoT sensors or CSV files.  
2. **Data Preprocessing** – Cleaning, formatting timestamps, and aggregation by day.  
3. **Feature Engineering** – Add `Date`, `Day_Index`, `Usage_kWh`, and `Cost(INR)` columns.  
4. **Model Training** – Fit a **Linear Regression** model on daily total usage.  
5. **Prediction** – Forecast next 10 days of electricity consumption.  
6. **Visualization** – Plot actual vs. predicted usage using Matplotlib/Plotly.  

🧾 Example Code (Forecasting Section):

 python
# Aggregate usage by day
daily_df = df.groupby('Date')['Usage_kWh'].sum().reset_index()
daily_df['Day_Index'] = np.arange(len(daily_df))

# Train Linear Regression model
model = LinearRegression()
model.fit(daily_df[['Day_Index']], daily_df['Usage_kWh'])

# Forecast next 10 days
future_index = np.arange(len(daily_df), len(daily_df) + 10).reshape(-1, 1)
future_usage = model.predict(future_index)
future_dates = pd.date_range(start=daily_df['Date'].max() + pd.Timedelta(days=1), periods=10)

# Combine forecast data
future_df = pd.DataFrame({'Date': future_dates, 'Predicted_Usage_kWh': future_usage})

🧠 Insights & Benefits:

1.Identify which appliances consume the most energy.
2.Plan electricity usage to reduce bills.
3.Detect unusual consumption patterns.
4.Promote eco-friendly energy habits.

🏁 Conclusion:

EcoWatts – Smart Home Energy Analyzer is an intelligent solution for understanding and optimizing electricity usage.
By combining machine learning forecasting with visual analytics, it enables households to achieve sustainable energy consumption and cost efficiency.
