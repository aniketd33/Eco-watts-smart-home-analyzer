import matplotlib.pyplot as plt
import pandas as pd

# -----------------------------------
# 1️⃣ Appliance-wise Energy Usage
# -----------------------------------
def plot_usage_by_appliance(df):
    """Bar chart showing total energy usage by each appliance."""
    if "Appliance" not in df.columns:
        raise ValueError("Missing column: Appliance")

    appliance_usage = df.groupby("Appliance")["Usage_kWh"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(6, 4))
    appliance_usage.plot(kind="bar", color="#2b9348", ax=ax)
    ax.set_title("Appliance-wise Energy Usage", fontsize=12, fontweight="bold", color="#1b4332")
    ax.set_xlabel("Appliance", fontsize=10)
    ax.set_ylabel("Energy Used (kWh)", fontsize=10)
    ax.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    return fig


# -----------------------------------
# 2️⃣ Daily Energy Cost Trend
# -----------------------------------
def plot_daily_cost_trend(df):
    """Line chart showing daily energy cost trends."""
    if "Timestamp" not in df.columns or "Cost(INR)" not in df.columns:
        raise ValueError("Missing columns: Timestamp or Cost(INR)")

    df["Date"] = pd.to_datetime(df["Timestamp"]).dt.date
    daily_cost = df.groupby("Date")["Cost(INR)"].sum()

    fig, ax = plt.subplots(figsize=(6, 4))
    daily_cost.plot(ax=ax, marker="o", color="#007f5f", linewidth=2)
    ax.set_title("Daily Energy Cost Trend", fontsize=12, fontweight="bold", color="#1b4332")
    ax.set_xlabel("Date", fontsize=10)
    ax.set_ylabel("Total Cost (INR)", fontsize=10)
    plt.xticks(rotation=45)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    return fig


# -----------------------------------
# 3️⃣ Room-wise Energy Usage (Pie)
# -----------------------------------
def plot_room_wise_usage(df):
    """Pie chart showing percentage of total energy usage by room."""
    if "Room" not in df.columns:
        raise ValueError("Missing column: Room")

    room_usage = df.groupby("Room")["Usage_kWh"].sum()
    fig, ax = plt.subplots(figsize=(6, 4))
    colors = plt.cm.Greens.colors

    ax.pie(
        room_usage,
        labels=room_usage.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors,
        wedgeprops={"edgecolor": "white", "linewidth": 1}
    )
    ax.set_title("Room-wise Energy Usage", fontsize=12, fontweight="bold", color="#1b4332")
    plt.tight_layout()
    return fig



