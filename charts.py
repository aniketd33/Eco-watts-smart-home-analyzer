import matplotlib.pyplot as plt

# -------------------------------
# 🔌 Appliance-wise Energy Usage
# -------------------------------
def plot_usage_by_appliance(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    df.groupby('Appliance')['Usage_kWh'].sum().plot(
        kind='bar',
        ax=ax,
        color='#42A5F5',
        edgecolor='black'
    )
    ax.set_title('Appliance-wise Energy Usage', fontsize=12, fontweight='bold')
    ax.set_ylabel('Usage (kWh)')
    ax.set_xlabel('Appliance')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig


# -------------------------------
# 💰 Daily Energy Cost Trend
# -------------------------------
def plot_daily_cost_trend(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    df['Date'] = df['Timestamp'].dt.date
    daily_cost = df.groupby('Date')['Cost(INR)'].sum()
    daily_cost.plot(
        ax=ax,
        color='#66BB6A',
        linewidth=2,
        marker='o'
    )
    ax.set_title('Daily Energy Cost Trend', fontsize=12, fontweight='bold')
    ax.set_ylabel('Cost (INR)')
    ax.set_xlabel('Date')

    # Rotate and format date labels to avoid overlap
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    return fig


# -------------------------------
# 🏠 Room-wise Energy Usage
# -------------------------------
def plot_room_wise_usage(df):
    """Displays total energy usage per room."""
    if 'Room' not in df.columns or 'Usage_kWh' not in df.columns:
        raise ValueError("Dataset must contain 'Room' and 'Usage_kWh' columns.")

    fig, ax = plt.subplots(figsize=(6, 4))
    df.groupby('Room')['Usage_kWh'].sum().plot(
        kind='bar',
        ax=ax,
        color='#FFA726',
        edgecolor='black'
    )
    ax.set_title('Room-wise Energy Usage', fontsize=12, fontweight='bold')
    ax.set_ylabel('Usage (kWh)')
    ax.set_xlabel('Room')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig



