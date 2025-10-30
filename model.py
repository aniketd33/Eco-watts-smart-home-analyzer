import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import plotly.graph_objects as go

def prepare_forecast_data(df):
    df['Date'] = df['Timestamp'].dt.date
    daily_data = df.groupby('Date')['Usage_kWh'].sum().reset_index()
    daily_data['Day'] = range(len(daily_data))
    return daily_data

def train_forecast_model(daily_data):
    X = daily_data[['Day']]
    y = daily_data['Usage_kWh']
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    mae = mean_absolute_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    return model, mae, r2

def forecast_next_days(model, daily_data, n_days=7):
    future_days = pd.DataFrame({'Day': range(len(daily_data), len(daily_data) + n_days)})
    future_pred = model.predict(future_days)
    forecast_df = pd.DataFrame({
        'Date': pd.date_range(daily_data['Date'].iloc[-1], periods=n_days + 1, freq='D')[1:],
        'Predicted_Usage': future_pred
    })
    return forecast_df

def plot_forecast_results(daily_data, forecast_df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=daily_data['Date'], y=daily_data['Usage_kWh'],
                             mode='lines+markers', name='Actual Usage', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=forecast_df['Date'], y=forecast_df['Predicted_Usage'],
                             mode='lines+markers', name='Forecast', line=dict(color='orange', dash='dash')))
    fig.update_layout(title="Energy Usage Forecast (Next 7 Days)",
                      xaxis_title="Date", yaxis_title="Usage (kWh)",
                      template="plotly_white")
    return fig
