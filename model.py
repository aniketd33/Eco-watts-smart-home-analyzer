import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import plotly.graph_objects as go
import plotly.express as px

# ---------------------------------------------------
# 🧩 Function: Prepare data for forecasting
# ---------------------------------------------------
def prepare_forecast_data(df, date_col='Timestamp', usage_col='Usage_kWh'):
    """
    Prepare time series data for forecasting energy usage.
    Converts dates to numeric format for regression modeling.
    """
    df[date_col] = pd.to_datetime(df[date_col])
    daily_usage = df.groupby(df[date_col].dt.date)[usage_col].sum().reset_index()
    daily_usage.rename(columns={date_col: 'Date'}, inplace=True)
    daily_usage['DayIndex'] = np.arange(len(daily_usage))  # used as X for regression

    return daily_usage


# ---------------------------------------------------
# 🔮 Function: Train Linear Regression Model
# ---------------------------------------------------
def train_forecast_model(daily_usage):
    """
    Trains a Linear Regression model to predict future energy usage.
    """
    X = daily_usage[['DayIndex']]
    y = daily_usage['Usage_kWh']

    model = LinearRegression()
    model.fit(X, y)

    # Metrics
    y_pred = model.predict(X)
    mae = mean_absolute_error(y, y_pred)
    r2 = r2_score(y, y_pred)

    return model, mae, r2


# ---------------------------------------------------
# 📅 Function: Generate 7-day forecast
# ---------------------------------------------------
def forecast_next_days(model, daily_usage, n_days=7):
    """
    Generates a forecast for the next n_days based on trained model.
    """
    last_index = daily_usage['DayIndex'].iloc[-1]
    future_indices = np.arange(last_index + 1, last_index + n_days + 1)
    future_dates = pd.date_range(start=daily_usage['Date'].iloc[-1], periods=n_days + 1, freq='D')[1:]

    forecast_values = model.predict(future_indices.reshape(-1, 1))

    forecast_df = pd.DataFrame({
        'Date': future_dates,
        'Predicted_Usage_kWh': forecast_values
    })

    return forecast_df


# ---------------------------------------------------
# 📊 Function: Plot Forecast Results
# ---------------------------------------------------
def plot_forecast_results(actual_df, forecast_df):
    """
    Visualizes actual vs predicted energy usage.
    """
    fig = go.Figure()

    # Actual Data
    fig.add_trace(go.Scatter(
        x=actual_df['Date'],
        y=actual_df['Usage_kWh'],
        mode='lines+markers',
        name='Actual Usage',
        line=dict(color='#2E8B57', width=3)
    ))

    # Forecast Data
    fig.add_trace(go.Scatter(
        x=forecast_df['Date'],
        y=forecast_df['Predicted_Usage_kWh'],
        mode='lines+markers',
        name='Forecast (Next 7 Days)',
        line=dict(color='#FFB84C', dash='dash', width=3)
    ))

    fig.update_layout(
        title='⚙️ Energy Usage Forecast (Next 7 Days)',
        xaxis_title='Date',
        yaxis_title='Energy Usage (kWh)',
        template='plotly_white',
        legend_title='Legend',
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis_tickangle=-45
    )

    return fig
