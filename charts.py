import matplotlib.pyplot as plt

def plot_usage_by_appliance(df):
    fig, ax = plt.subplots()
    df.groupby('Appliance')['Usage_kWh'].sum().plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title('Energy Usage by Appliance')
    ax.set_ylabel('Usage (kWh)')
    ax.set_xlabel('Appliance')
    return fig


def plot_daily_cost_trend(df):
    fig, ax = plt.subplots()
    df['Date'] = df['Timestamp'].dt.date
    daily_cost = df.groupby('Date')['Cost(INR)'].sum()
    daily_cost.plot(ax=ax, color='orange')
    ax.set_title('Daily Energy Cost Trend')
    ax.set_ylabel('Cost (INR)')
    ax.set_xlabel('Date')
    return fig


# ✅ FIXED FUNCTION BELOW
def plot_temp_vs_usage(df, temp_col='Temp(C)', usage_col='Usage_kWh'):
    """
    Plots the relationship between temperature and energy usage.
    Works even if column names differ (like Temperature or Usage).
    """
    if temp_col not in df.columns or usage_col not in df.columns:
        # Try to auto-detect columns
        temp_candidates = [c for c in df.columns if 'temp' in c.lower()]
        usage_candidates = [c for c in df.columns if 'usage' in c.lower()]
        if temp_candidates and usage_candidates:
            temp_col = temp_candidates[0]
            usage_col = usage_candidates[0]
        else:
            raise ValueError("Temperature or Usage column not found in dataset.")

    fig, ax = plt.subplots()
    ax.scatter(df[temp_col], df[usage_col], color='green', alpha=0.6)
    ax.set_title('Temperature vs Energy Usage')
    ax.set_xlabel(f'{temp_col}')
    ax.set_ylabel(f'{usage_col}')
    return fig

