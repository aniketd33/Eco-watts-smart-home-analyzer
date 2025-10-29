import matplotlib.pyplot as plt

# ----------------------------
# Appliance Usage Chart
# ----------------------------
def plot_usage_by_appliance(df):
    fig, ax = plt.subplots(figsize=(5, 3))
    bars = df.groupby('Appliance')['Usage_kWh'].sum().sort_values(ascending=False).plot(
        kind='bar',
        ax=ax,
        color='#42A5F5',
        edgecolor='black'
    )

    for p in bars.patches:
        ax.annotate(
            f"{p.get_height():.1f}",
            (p.get_x() + p.get_width() / 2, p.get_height()),
            ha='center', va='bottom', fontsize=8, color='black'
        )

    ax.set_title('🔌 Energy Usage by Appliance', fontsize=11, fontweight='bold', pad=10)
    ax.set_ylabel('Usage (kWh)', fontsize=9)
    ax.set_xlabel('Appliance', fontsize=9)
    plt.xticks(rotation=30, ha='right')
    plt.grid(True, axis='y', linestyle='--', alpha=0.4)
    plt.tight_layout(pad=1)
    return fig

# ----------------------------
# Daily Cost Trend Chart
# ----------------------------
def plot_daily_cost_trend(df):
    fig, ax = plt.subplots(figsize=(5, 3))
    df['Date'] = df['Timestamp'].dt.date
    daily_cost = df.groupby('Date')['Cost(INR)'].sum()
    daily_cost.plot(ax=ax, color='#FFA726', linewidth=2, marker='o')

    ax.set_title('📅 Daily Energy Cost Trend', fontsize=11, fontweight='bold', pad=10)
    ax.set_ylabel('Cost (INR)', fontsize=9)
    ax.set_xlabel('Date', fontsize=9)
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout(pad=1)
    return fig

# ----------------------------
# Room-wise Usage Chart
# ----------------------------
def plot_room_wise_usage(df):
    """Displays total energy usage per room in compact professional style."""
    if 'Room' not in df.columns or 'Usage_kWh' not in df.columns:
        raise ValueError("Dataset must contain 'Room' and 'Usage_kWh' columns.")

    fig, ax = plt.subplots(figsize=(5, 3))  # compact chart size
    bars = df.groupby('Room')['Usage_kWh'].sum().plot(
        kind='bar',
        ax=ax,
        color='#FFB74D',
        edgecolor='black'
    )

    for p in bars.patches:
        ax.annotate(
            f"{p.get_height():.1f}",
            (p.get_x() + p.get_width() / 2, p.get_height()),
            ha='center',
            va='bottom',
            fontsize=8,
            color='black'
        )

    ax.set_title('🏠 Room-wise Energy Usage', fontsize=11, fontweight='bold', pad=10)
    ax.set_ylabel('Usage (kWh)', fontsize=9)
    ax.set_xlabel('Room', fontsize=9)
    plt.xticks(rotation=30, ha='right')
    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout(pad=1)
    return fig



