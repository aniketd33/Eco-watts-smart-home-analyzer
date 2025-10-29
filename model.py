
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error

def load_and_preprocess(df):
    # Aggregate to daily usage
    df['date'] = df['Timestamp'].dt.date
    daily = df.groupby('date').agg({'Usage_kWh':'sum'}).reset_index()
    daily['date'] = pd.to_datetime(daily['date'])
    daily = daily.sort_values('date')
    X = np.arange(len(daily)).reshape(-1,1)  # simple numeric time index
    y = daily['Usage_kWh'].values
    return X, y, daily

def train_and_predict(X, y, periods=7, df_daily=None):
    model = LinearRegression()
    model.fit(X, y)
    # Metrics on train
    y_pred = model.predict(X)
    metrics = {
        'r2_score': float(r2_score(y, y_pred)),
        'mae': float(mean_absolute_error(y, y_pred))
    }
    # Forecast next `periods` days using linear extrapolation on index
    last_idx = X[-1,0]
    future_idx = np.arange(last_idx+1, last_idx+periods+1).reshape(-1,1)
    future_pred = model.predict(future_idx)
    future_dates = pd.date_range(start=df_daily['date'].max() + pd.Timedelta(days=1), periods=periods)
    pred_df = pd.DataFrame({'date': future_dates, 'predicted_usage': future_pred})
    return pred_df, metrics
