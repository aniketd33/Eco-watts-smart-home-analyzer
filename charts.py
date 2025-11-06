import matplotlib.pyplot as plt
import pandas as pd

# -------------------------------
# 1️⃣ Usage by Appliance
# -------------------------------
def plot_usage_by_appliance(df):
    """Bar chart showing total energy usage by each appliance."""
    appliance_usage = df.groupby("Appliance")["Usage_kWh"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots()
    appliance_usage.plot(kind="bar", color="#52b788", ax=ax)
    ax.set_title("Appliance-wise Energy Usage")
    ax.set_xlabel("Appliance")
    ax.set_ylabel("Energy Used (kWh)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    return fig

# -------------------------------
# 2️⃣ Daily Cost Trend
# -------------------------------
def plot_daily_cost_trend(df):
    """Line chart showing total daily energy cost."""
    df["Date"] = pd.to_datetime(df["Timestamp"]).dt.date
    daily_cost = df.groupby("Date")["Cost(INR)"].sum()
    fig, ax = plt.subplots()
    daily_cost.plot(kind="line", marker="o", color="#40916c", ax=ax)
    ax.set_title("Daily Energy Cost Trend")
    ax.set_xlabel("Date")
    ax.set_ylabel("Cost (INR)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    return fig

# -------------------------------
# 3️⃣ Room-wise Usage
# -------------------------------
def plot_room_wise_usage(df):
    """Pie chart for energy consumption by room."""
    if "Room" not in df.columns:
        raise ValueError("Room column not found in dataset.")
    room_usage = df.groupby("Room")["Usage_kWh"].sum()
    fig, ax = plt.subplots()
    ax.pie(room_usage, labels=room_usage.index, autopct="%1.1f%%", colors=plt.cm.Greens.colors)
    ax.set_title("Room-wise Energy Usage")
    plt.tight_layout()
    return fig


