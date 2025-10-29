import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# Apply a consistent, clean style
plt.style.use('seaborn-v0_8-whitegrid')

# -------------------------------------------------
# 1️⃣ Energy Usage by Appliance
# -------------------------------------------------
def plot_usage_by_appliance(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    usage = df.groupby('Appliance')['Usage_kWh'].sum().sort_values(ascending=False)
    usage.plot(kind='bar', ax=ax, color='#4FA7B9', edgecolor='black')

    ax.set_title('🔌 Energy Usage by Appliance', fontsize=12, weight='bold')
    ax.set_ylabel('Usage (kWh)', fontsize=10)
    ax.set_xlabel('Appliance', fontsize=10)
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, linestyle='--', alpha=0.5)
    fig.tight_layout()
    return fig


# -------------------------------------------------
# 2️⃣ Daily Energy Cost Trend
# -------------------------------------------------
def plot_daily_cost_trend(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    df['Date'] = df['Timestamp'].dt.date
    daily_cost = df.groupby('Date')['Cost(INR)'].sum()
    ax.plot(daily_cost.index, daily_cost.values, marker='o', color='#F5A623', linewidth=2)

    ax.set_title('💰 Daily Energy Cost Trend', fontsize=12, weight='bold')
    ax.set_ylabel('Cost (INR)', fontsize=10)
    ax.set_xlabel('Date', fontsize=10)
    ax.xaxis.set_major_locator(plt.MaxNLocator(6))  # Show fewer x-labels
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))
    ax.grid(True, linestyle='--', alpha=0.5)
    fig.tight_layout()
    return fig


# -------------------------------------------------
# 3️⃣ Temperature vs Energy Usage (Dynamic)
# -------------------------------------------------
def plot_temp_vs_usage(df, temp_col='Temp(C)', usage_col='Usage_kWh'):
    """
    Plots the relationship between temperature and energy usage.
    Automatically detects columns if names differ.
    """
    # Auto-detect column names if necessary
    if temp_col not in df.columns or usage_col not in df.columns:
        temp_candidates = [c for c in df.columns if 'temp' in c.lower()]
        usage_candidates = [c for c in df.columns if 'usage' in c.lower()]
        if temp_candidates and usage_candidates:
            temp_col = temp_candidates[0]
            usage_col = usage_candidates[0]
        else:
            raise ValueError("Temperature or Usage column not found in dataset.")

    # Create scatter plot
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(df[temp_col], df[usage_col], color='#7AC142', alpha=0.7, edgecolors='black', linewidths=0.5)

    ax.set_title('🌡️ Temperature vs Energy Usage', fontsize=12, weight='bold')
    ax.set_xlabel(f'{temp_col}', fontsize=10)
    ax.set_ylabel(f'{usage_col}', fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.5)
    fig.tight_layout()
    return fig


