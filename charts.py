import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Apply Seaborn Theme for uniform professional look
sns.set_theme(style="whitegrid")

# ----------------------------------------------------------
# 📊 1. Energy Usage by Appliance
# ----------------------------------------------------------
def plot_usage_by_appliance(df):
    fig, ax = plt.subplots(figsize=(7, 4))
    data = df.groupby("Appliance")["Usage_kWh"].sum().sort_values(ascending=False)
    
    bars = sns.barplot(x=data.values, y=data.index, palette="crest", ax=ax)
    ax.set_title("🔌 Energy Usage by Appliance", fontsize=13, color="#2b6777", weight="bold")
    ax.set_xlabel("Total Usage (kWh)", fontsize=11)
    ax.set_ylabel("Appliance", fontsize=11)

    # Annotate values on bars
    for bar in bars.patches:
        ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
                f'{bar.get_width():.1f}', va='center', fontsize=9, color='#333')

    plt.tight_layout()
    return fig


# ----------------------------------------------------------
# 💰 2. Daily Energy Cost Trend
# ----------------------------------------------------------
def plot_daily_cost_trend(df):
    fig, ax = plt.subplots(figsize=(7, 4))
    df["Date"] = df["Timestamp"].dt.date
    daily_cost = df.groupby("Date")["Cost(INR)"].sum()

    ax.plot(daily_cost.index, daily_cost.values, color="#52b788", marker="o", linewidth=2)
    ax.set_title("💰 Daily Energy Cost Trend", fontsize=13, color="#2b6777", weight="bold")
    ax.set_xlabel("Date", fontsize=11)
    ax.set_ylabel("Cost (INR)", fontsize=11)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


# ----------------------------------------------------------
# 🏠 3. Room-wise Energy Usage
# ----------------------------------------------------------
def plot_room_wise_usage(df):
    fig, ax = plt.subplots(figsize=(7, 4))
    room_data = df.groupby("Room")["Usage_kWh"].sum().sort_values(ascending=False)

    colors = sns.color_palette("coolwarm", len(room_data))
    bars = ax.bar(room_data.index, room_data.values, color=colors, alpha=0.85)

    ax.set_title("🏠 Room-wise Energy Usage", fontsize=13, color="#2b6777", weight="bold")
    ax.set_xlabel("Room", fontsize=11)
    ax.set_ylabel("Usage (kWh)", fontsize=11)
    plt.xticks(rotation=45)

    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                f'{bar.get_height():.1f}', ha='center', fontsize=9, color='#333')

    plt.tight_layout()
    return fig




