import pandas as pd
import plotly.graph_objects as go
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.linear_model import LinearRegression
import numpy as np


# -------------------------------------------
# Prepare Forecast Data
# -------------------------------------------
def prepare_forecast_data(df):
    df_daily = df.groupby(df["Timestamp"].dt.date)["Usage_kWh"].sum().reset_index()
    df_daily.columns = ["date", "usage"]
    df_daily["day_num"] = np.arange(len(df_daily))
    return df_daily


# -------------------------------------------
# Train Model
# -------------------------------------------
def train_forecast_model(df_daily):
    X = df_daily[["day_num"]]
    y = df_daily["usage"]

    model = LinearRegression()
    model.fit(X, y)

    preds = model.predict(X)
    mae = mean_absolute_error(y, preds)
    r2 = r2_score(y, preds)

    return model, mae, r2


# -------------------------------------------
# Forecast Next Days (Updated to 20 days)
# -------------------------------------------
def forecast_next_days(model, df_daily, days=20):  # <-- UPDATED
    last_day = df_daily["day_num"].max()
    future_days = np.arange(last_day + 1, last_day + days + 1)

    predicted = model.predict(future_days.reshape(-1, 1))
    forecast_df = pd.DataFrame({
        "date": pd.date_range(start=df_daily["date"].iloc[-1], periods=days+1)[1:],
        "predicted_usage": predicted
    })
    return forecast_df


# -------------------------------------------
# Plot Forecast Results
# -------------------------------------------
def plot_forecast_results(df_daily, forecast_df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_daily["date"], y=df_daily["usage"],
        mode="lines+markers", name="Actual Usage"
    ))

    fig.add_trace(go.Scatter(
        x=forecast_df["date"], y=forecast_df["predicted_usage"],
        mode="lines+markers", name="Forecasted Usage"
    ))

    fig.update_layout(
        title="Energy Usage Forecast (Next 20 Days)",
        xaxis_title="Date",
        yaxis_title="Usage (kWh)",
        template="plotly_white"
    )
    return fig
