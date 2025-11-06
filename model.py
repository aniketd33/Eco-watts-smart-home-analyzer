import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import plotly.graph_objects as go
import numpy as np


# ---------------------------------
# 📅 Step 1: Prepare Forecast Data
# ---------------------------------
def prepare_forecast_data(df):
    df["Date"] = df["Timestamp"].dt.date
    daily_usage = df.groupby("Date")["Usage_kWh"].sum().reset_index()
    daily_usage["Day_Index"] = np.arange(len(daily_usage))
    return daily_usage


# ---------------------------------
# 🧠 Step 2: Train Forecast Model
# ---------------------------------
def train_forecast_model(daily_usage):
    X = daily_usage[["Day_Index"]]
    y = daily_usage["Usage_kWh"]
    model = LinearRegression()
    model.fit(X, y)

    preds = model.predict(X)
    mae = mean_absolute_error(y, preds)
    r2 = r2_score(y, preds)
    return model, mae, r2


# ---------------------------------
# 🔮 Step 3: Forecast Future Usage
# ---------------------------------
def forecast_next_days(model, daily_usage, days_ahead=7):
    last_index = daily_usage["Day_Index"].max()
    future_idx = np.arange(last_index + 1, last_index + days_ahead + 1)
    future_pred = model.predict(future_idx.reshape(-1, 1))

    forecast_df = pd.DataFrame({
        "Date": pd.date_range(
            start=pd.to_datetime(daily_usage["Date"].max()) + pd.Timedelta(days=1),
            periods=days_ahead
        ),
        "Predicted_Usage_kWh": future_pred
    })
    return forecast_df


# ---------------------------------
# 📉 Step 4: Plot Forecast Results
# ---------------------------------
def plot_forecast_results(daily_usage, forecast_df):
    fig = go.Figure()

    # Historical Data
    fig.add_trace(go.Scatter(
        x=daily_usage["Date"], y=daily_usage["Usage_kWh"],
        mode="lines+markers", name="Actual Usage",
        line=dict(color="#0077b6", width=3)
    ))

    # Forecasted Data
    fig.add_trace(go.Scatter(
        x=forecast_df["Date"], y=forecast_df["Predicted_Usage_kWh"],
        mode="lines+markers", name="Forecasted Usage",
        line=dict(color="#ffb703", dash="dash", width=3)
    ))

    fig.update_layout(
        title="🔮 Energy Usage Forecast (Next 7 Days)",
        xaxis_title="Date",
        yaxis_title="Energy Usage (kWh)",
        template="plotly_white",
        legend=dict(bgcolor="white", bordercolor="#d9d9d9", borderwidth=1),
        height=400
    )
    return fig

