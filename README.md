🌿 EcoWatts – Smart Home Energy Analyzer
🏷️ Title
EcoWatts – Smart Home Energy Analyzer

🧭 Overview
EcoWatts is a data-driven web application designed to monitor, analyze, and optimize household electricity consumption. The system helps users identify high-energy-consuming appliances, track daily/weekly usage trends, and receive actionable insights for saving energy and reducing electricity bills. Using real-time analytics and predictive modeling, EcoWatts promotes sustainable living and efficient energy management.

⚙️ Features
Energy Usage Dashboard – Interactive visualization of appliance-wise and room-wise electricity consumption.
Cost Estimation – Calculates estimated energy costs based on kWh usage and tariff rates.
Forecasting Model – Uses Linear Regression to predict future electricity consumption trends.
Real-Time Data Upload – Supports CSV input of appliance usage data for analysis.
Eco-Tips Generator – Suggests personalized, eco-friendly energy-saving recommendations.
User-Friendly Interface – Built using Streamlit for an intuitive, responsive design.
Downloadable Reports – Generates summary reports in CSV or PDF format.
🧩 Dataset
Name: energy_usage_Dataset.csv

Description:
Contains timestamped appliance usage data with the following columns:

Timestamp
Appliance
Usage_kWh
Room
Mode
Temperature (°C)
Cost (INR)
Size: 200 records
Source: Custom dataset or open-source (Kaggle / simulated IoT smart home dataset)

💻 Tech Stack
Component	Technology
Frontend	Streamlit
Backend	Python (Pandas, NumPy)
Visualization	Matplotlib, Plotly, Seaborn
Machine Learning	Scikit-learn (Linear Regression)
Storage	CSV / Local DB
Deployment	Streamlit Cloud / GitHub Pages
🤖 Model Summary
Algorithm Used: Linear Regression
Objective: Predict future energy consumption based on past usage patterns.
Input Features: Time, appliance type, temperature, mode.
Output: Forecasted energy usage (kWh).
Performance Metrics: R² Score, Mean Absolute Error (MAE).
🗓️ Project Timeline (2 Weeks)
Week	Task Description
Week 1	Data collection, cleaning, preprocessing, and exploratory data analysis (EDA). Build visualization dashboard using Streamlit.
Week 2	Implement Linear Regression model, integrate insights into dashboard, deploy final app, and perform testing.
🚀 Future Improvements
Integrate IoT sensor data for real-time tracking.
Add deep learning models (LSTM) for time-series forecasting.
Build mobile app version for real-time monitoring.
Include carbon footprint tracking and renewable energy comparison.
Add alerts/notifications for excessive power usage.
👨‍💻 Author
Aniket Dombale
Department of Technology, Savitribai Phule Pune University

📜 License
MIT License
This project is open-source and free to use, modify, and distribute for academic and research purposes with proper attribution.
