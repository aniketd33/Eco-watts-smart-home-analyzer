import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import numpy as np

def prepare_forecast_data(df):
    daily = df.groupby(df["Timestamp"].dt.date)["Usage_kWh"].sum().reset_index()
    daily.columns = ["Date", "Usage_kWh"]
    daily["Day_Index"] = range(len(daily))
    return daily

def train_forecast_model(data):
    X = data[["Day_Index"]]
    y = data["Usage_kWh"]

    model = LinearRegression()
    model.fit(X, y)
    preds = model.predict(X)

    mae = mean_absolute_error(y, preds)
    r2 = r2_score(y, preds)

    return model, mae, r2

def forecast_next_days(model, data, days_ahead=7):
    last_index = data["Day_Index"].max()
    future_days = np.arange(last_index + 1, last_index + 1 + days_ahead)
    preds = model.predict(future_days.reshape(-1, 1))

    forecast = pd.DataFrame({
        "Date": pd.date_range(start=data["Date"].iloc[-1], periods=days_ahead + 1, freq="D")[1:],
        "Predicted_Usage_kWh": preds
    })
    return forecast

def plot_forecast_results(data, forecast):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data["Date"], y=data["Usage_kWh"], mode="lines+markers",
                             name="Actual Usage", line=dict(color="#00796b")))
    fig.add_trace(go.Scatter(x=forecast["Date"], y=forecast["Predicted_Usage_kWh"],
                             mode="lines+markers", name="Forecast",
                             line=dict(color="#ff7043", dash="dash")))

    fig.update_layout(title="Energy Usage Forecast (Next 7 Days)",
                      xaxis_title="Date", yaxis_title="Energy Usage (kWh)",
                      template="plotly_white")
    return fig

