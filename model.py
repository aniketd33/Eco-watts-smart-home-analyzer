import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import plotly.graph_objects as go

def prepare_forecast_data(df):
    df["Date"] = df["Timestamp"].dt.date
    daily_data = df.groupby("Date")["Usage_kWh"].sum().reset_index()
    daily_data["Day"] = np.arange(len(daily_data))
    return daily_data

def train_forecast_model(daily_data):
    X = daily_data[["Day"]]
    y = daily_data["Usage_kWh"]
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    return model, mean_absolute_error(y, y_pred), r2_score(y, y_pred)

def forecast_next_days(model, daily_data, days_ahead=7):
    last_day = daily_data["Day"].iloc[-1]
    future_days = np.arange(last_day + 1, last_day + days_ahead + 1).reshape(-1, 1)
    preds = model.predict(future_days)
    future_dates = pd.date_range(daily_data["Date"].iloc[-1] + pd.Timedelta(days=1), periods=days_ahead)
    return pd.DataFrame({"Date": future_dates, "Predicted_Usage_kWh": preds})

def plot_forecast_results(daily_data, forecast_df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=daily_data["Date"], y=daily_data["Usage_kWh"], mode="lines+markers",
                             name="Actual", line=dict(color="#2b6777", width=3)))
    fig.add_trace(go.Scatter(x=forecast_df["Date"], y=forecast_df["Predicted_Usage_kWh"], mode="lines+markers",
                             name="Forecast", line=dict(color="#52b788", dash="dash", width=3)))
    fig.update_layout(title="🔮 Energy Usage Forecast", xaxis_title="Date", yaxis_title="kWh", template="plotly_white")
    return fig
