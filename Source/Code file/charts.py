
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='whitegrid')

def plot_usage_by_appliance(df):
    usage_by_app = df.groupby('Appliance')['Usage_kWh'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8,5))
    sns.barplot(x=usage_by_app.values, y=usage_by_app.index, ax=ax)
    ax.set_title('Total Energy Usage by Appliance')
    ax.set_xlabel('Total Usage (kWh)')
    ax.set_ylabel('Appliance')
    plt.tight_layout()
    return fig

def plot_daily_cost_trend(df):
    df['date'] = df['Timestamp'].dt.date
    if 'Cost(INR)' in df.columns:
        daily_cost = df.groupby('date')['Cost(INR)'].sum()
    elif 'Cost' in df.columns:
        daily_cost = df.groupby('date')['Cost'].sum()
    else:
        daily_cost = df.groupby('date')['Usage_kWh'].sum() * 0  # placeholder zeros
    fig, ax = plt.subplots(figsize=(8,4))
    ax.plot(daily_cost.index, daily_cost.values, marker='o')
    ax.set_title('Daily Energy Cost Trend')
    ax.set_xlabel('Date')
    ax.set_ylabel('Total Cost (INR)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def plot_temp_vs_usage(df):
    fig, ax = plt.subplots(figsize=(8,5))
    if 'Temperature (°C)' in df.columns:
        sns.scatterplot(data=df, x='Temperature (°C)', y='Usage_kWh', hue='Appliance', ax=ax, legend=False)
        ax.set_title('Temperature vs Energy Usage')
        ax.set_xlabel('Temperature (°C)')
        ax.set_ylabel('Usage (kWh)')
    else:
        ax.text(0.5, 0.5, 'Temperature column not found', ha='center')
    plt.tight_layout()
    return fig
