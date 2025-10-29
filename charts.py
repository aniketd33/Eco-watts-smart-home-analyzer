import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.dates as mdates

plt.style.use('seaborn-v0_8-whitegrid')

# 1️⃣ Appliance-wise Usage
def plot_usage_by_appliance(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    usage = df.groupby('Appliance')['Usage_kWh'].sum().sort_values(ascending=False)
    usage.plot(kind='bar', ax=ax, color='#4FA7B9', edgecolor='black')

    ax.set_title('🔌 Energy Usage by Appliance', fontsize=12, weight='bold')
    ax.set_ylabel('Usage (kWh)')
    ax.set_xlabel('Appliance')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, linestyle='--', alpha=0.5)
    fig.tight_layout()
    return fig


# 2️⃣ Daily Cost Trend (with fixed overlapping dates)
def plot_daily_cost_trend(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    df['Date'] = df['Timestamp'].dt.date
    daily_cost = df.groupby('Date')['Cost(INR)'].sum()

    ax.plot(daily_cost.index, daily_cost.values, marker='o', color='#F5A623', linewidth=2)
    ax.set_title('💰 Daily Energy Cost Trend', fontsize=12, weight='bold')
    ax.set_ylabel('Cost (INR)')
    ax.set_xlabel('Date')
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))

    fig.autofmt_xdate(rotation=45)
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
    ax.grid(True, linestyle='--', alpha=0.5)
    fig.tight_layout()
    return fig


# 3️⃣ Room-wise Usage (New Chart)
def plot_room_wise_usage(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    room_usage = df.groupby('Room')['Usage_kWh'].sum().sort_values(ascending=False)
    room_usage.plot(kind='bar', ax=ax, color='#7AC142', edgecolor='black')

    ax.set_title('🏠 Room-wise Energy Usage', fontsize=12, weight='bold')
    ax.set_ylabel('Usage (kWh)')
    ax.set_xlabel('Room')
    ax.tick_params(axis='x', rotation=30)
    ax.grid(True, linestyle='--', alpha=0.5)
    fig.tight_layout()
    return fig


