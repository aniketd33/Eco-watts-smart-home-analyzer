import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import plotly.graph_objects as go


# -----------------------------------
# 1️⃣ Prepare Data for Forecasting
# -----------------------------------
def prepare_forecast_data(df):
    """Convert raw timestamp data into daily totals."""
    if "Timestamp" not in df.columns or "Usage_kWh" not in df.columns:
        raise ValueError("Dataset missing required columns (Timestamp, Usage_kWh)")

    df["Date"] = pd.to_datetime(df["Timestamp"]).dt.date
    daily_usage = df.groupby("Date")["Usage_kWh"].sum().reset_index()
    daily_usage["Day_Index"] = np.arange(len(daily_usage))
    return daily_usage


# -----------------------------------
# 2️⃣ Train Forecast Model
# -----------------------------------
def train_forecast_model(daily_usage):
    """Train Linear Regression model on daily usage."""
    X = daily_usage[["Day_Index"]]
    y = daily_usage["Usage_kWh"]

    model = LinearRegression()
    model.fit(X, y)

    y_pred = model.predict(X)
    mae = mean_absolute_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    return model, mae, r2


# -----------------------------------
# 3️⃣ Forecast Future Usage
# -----------------------------------
def forecast_next_days(model, daily_usage, future_days=7):
    """Generate predictions for the next given number of days."""
    last_day_index = daily_usage["Day_Index"].max()
    future_indices = np.arange(last_day_index + 1, last_day_index + future_days + 1)
    future_predictions = model.predict(future_indices.reshape(-1, 1))
    future_dates = pd.date_range(start=daily_usage["Date"].iloc[-1], periods=future_days + 1, closed="right")

    forecast_df = pd.DataFrame({
        "Date": future_dates,
        "Predicted_Usage_kWh": future_predictions
    })
    return forecast_df


# -----------------------------------
# 4️⃣ Plot Forecast Results
# -----------------------------------
def plot_forecast_results(daily_usage, forecast_df):
    """Plot actual vs predicted future energy usage."""
    fig = go.Figure()

    # Actual usage
    fig.add_trace(go.Scatter(
        x=daily_usage["Date"], y=daily_usage["Usage_kWh"],
        mode="lines+markers",
        name="Actual Usage (kWh)",
        line=dict(color="#007f5f", width=3)
    ))

    # Forecasted usage
    fig.add_trace(go.Scatter(
        x=forecast_df["Date"], y=forecast_df["Predicted_Usage_kWh"],
        mode="lines+markers",
        name="Forecast (Next Days)",
        line=dict(color="#80b918", width=3, dash="dash")
    ))

    fig.update_layout(
        title="Energy Consumption Forecast",
        xaxis_title="Date",
        yaxis_title="Energy Usage (kWh)",
        template="plotly_white",
        legend=dict(x=0, y=1.1, orientation="h"),
        height=500
    )
    return fig



