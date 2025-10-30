import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import numpy as np
import plotly.graph_objects as go

# -----------------------------------------------------
# 🧹 Prepare Data for Forecasting
# -----------------------------------------------------
def prepare_forecast_data(df):
    df["Date"] = pd.to_datetime(df["Timestamp"]).dt.date
    daily_usage = df.groupby("Date")["Usage_kWh"].sum().reset_index()
    daily_usage["DayIndex"] = np.arange(len(daily_usage))
    return daily_usage

# -----------------------------------------------------
# 🧠 Train Forecast Model (Linear Regression)
# -----------------------------------------------------
def train_forecast_model(daily_usage):
    X = daily_usage[["DayIndex"]]
    y = daily_usage["Usage_kWh"]

    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)

    mae = mean_absolute_error(y, y_pred)
    r2 = r2_score(y, y_pred)

    return model, mae, r2

# -----------------------------------------------------
# 🔮 Forecast Next 7 Days
# -----------------------------------------------------
def forecast_next_days(model, daily_usage, days_ahead=7):
    last_index = daily_usage["DayIndex"].max()
    future_indices = np.arange(last_index + 1, last_index + days_ahead + 1)
    forecast_values = model.predict(future_indices.reshape(-1, 1))
    forecast_dates = pd.date_range(start=daily_usage["Date"].iloc[-1], periods=days_ahead + 1, closed='right')
    
    forecast_df = pd.DataFrame({
        "Date": forecast_dates,
        "Forecast_Usage_kWh": forecast_values
    })
    return forecast_df

# -----------------------------------------------------
# 📈 Plot Forecast Results
# -----------------------------------------------------
def plot_forecast_results(daily_usage, forecast_df):
    fig = go.Figure()

    # Actual data
    fig.add_trace(go.Scatter(
        x=daily_usage["Date"], y=daily_usage["Usage_kWh"],
        mode="lines+markers", name="Actual Usage",
        line=dict(color="#2d6a4f", width=3)
    ))

    # Forecast data
    fig.add_trace(go.Scatter(
        x=forecast_df["Date"], y=forecast_df["Forecast_Usage_kWh"],
        mode="lines+markers", name="Forecasted Usage",
        line=dict(color="#74c69d", dash="dot", width=3)
    ))

    fig.update_layout(
        title="🔮 Energy Usage Forecast (Next 7 Days)",
        xaxis_title="Date",
        yaxis_title="Usage (kWh)",
        font=dict(family="Poppins", size=14, color="#1b4332"),
        template="plotly_white",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    return fig

