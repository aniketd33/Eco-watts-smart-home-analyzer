import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import plotly.graph_objects as go

# ------------------------------------------
# Prepare data for forecasting
# ------------------------------------------
def prepare_forecast_data(df):
    df["Date"] = pd.to_datetime(df["Timestamp"]).dt.date
    daily_usage = df.groupby("Date")["Usage_kWh"].sum().reset_index()
    daily_usage["Day_Index"] = np.arange(len(daily_usage))
    return daily_usage

# ------------------------------------------
# Train forecasting model
# ------------------------------------------
def train_forecast_model(daily_usage):
    X = daily_usage[["Day_Index"]]
    y = daily_usage["Usage_kWh"]
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    mae = mean_absolute_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    return model, mae, r2

# ------------------------------------------
# Forecast next few days
# ------------------------------------------
def forecast_next_days(model, daily_usage, future_days=7):
    last_day_index = daily_usage["Day_Index"].max()
    future_indices = np.arange(last_day_index + 1, last_day_index + future_days + 1)
    future_predictions = model.predict(future_indices.reshape(-1, 1))
    future_dates = pd.date_range(start=daily_usage["Date"].iloc[-1], periods=future_days + 1, closed="right")
    forecast_df = pd.DataFrame({"Date": future_dates, "Predicted_Usage_kWh": future_predictions})
    return forecast_df

# ------------------------------------------
# Plot forecast results
# ------------------------------------------
def plot_forecast_results(daily_usage, forecast_df):
    fig = go.Figure()

    # Actual usage
    fig.add_trace(go.Scatter(
        x=daily_usage["Date"], y=daily_usage["Usage_kWh"],
        mode="lines+markers", name="Actual Usage (kWh)",
        line=dict(color="#1b4332")
    ))

    # Forecasted usage
    fig.add_trace(go.Scatter(
        x=forecast_df["Date"], y=forecast_df["Predicted_Usage_kWh"],
        mode="lines+markers", name="Forecast (Next Days)",
        line=dict(color="#52b788", dash="dash")
    ))

    fig.update_layout(
        title="Energy Consumption Forecast",
        xaxis_title="Date",
        yaxis_title="Energy Used (kWh)",
        template="plotly_white"
    )
    return fig

