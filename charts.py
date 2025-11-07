import matplotlib.pyplot as plt
import pandas as pd

def plot_usage_by_appliance(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    df.groupby('Appliance')['Usage_kWh'].sum().sort_values().plot(
        kind='barh', color='#74c69d', ax=ax)
    ax.set_title('Energy Usage by Appliance', fontsize=12, fontweight='bold')
    ax.set_xlabel('Total Usage (kWh)')
    ax.set_ylabel('Appliance')
    plt.tight_layout()
    return fig


def plot_daily_cost_trend(df):
    df['Date'] = df['Timestamp'].dt.date
    daily_cost = df.groupby('Date')['Cost(INR)'].sum()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(daily_cost.index, daily_cost.values, color='#f9844a', marker='o')
    ax.set_title('Daily Energy Cost Trend', fontsize=12, fontweight='bold')
    ax.set_xlabel('Date')
    ax.set_ylabel('Cost (₹)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


def plot_room_wise_usage(df):
    if 'Room' not in df.columns:
        raise ValueError("Room column not found.")
    room_usage = df.groupby('Room')['Usage_kWh'].sum()
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.pie(room_usage, labels=room_usage.index, autopct='%1.1f%%', startangle=90,
           colors=['#52b788', '#95d5b2', '#c7f9cc', '#74c69d'])
    ax.set_title('Room-wise Energy Distribution', fontsize=12, fontweight='bold')
    plt.tight_layout()
    return fig


def plot_peak_usage_timeline(df):
    df['Hour'] = df['Timestamp'].dt.hour
    hourly_usage = df.groupby('Hour')['Usage_kWh'].sum()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(hourly_usage.index, hourly_usage.values, color='#40916c', linewidth=2, marker='o')
    ax.set_title('Hourly Peak Usage Timeline', fontsize=12, fontweight='bold')
    ax.set_xlabel('Hour of the Day')
    ax.set_ylabel('Usage (kWh)')
    plt.grid(alpha=0.3)
    plt.tight_layout()
    return fig



