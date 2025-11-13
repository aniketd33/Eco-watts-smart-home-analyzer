import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")


# ------------------------------------------------
# Appliance-wise Usage
# ------------------------------------------------
def plot_usage_by_appliance(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    df.groupby("Appliance")["Usage_kWh"].sum().plot(kind="bar", color="#2b6777", ax=ax)
    ax.set_title("Energy Usage by Appliance")
    ax.set_xlabel("Appliance")
    ax.set_ylabel("Usage (kWh)")
    plt.xticks(rotation=45)
    return fig


# ------------------------------------------------
# Daily Cost Trend
# ------------------------------------------------
def plot_daily_cost_trend(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    df["Date"] = df["Timestamp"].dt.date
    daily_cost = df.groupby("Date")["Cost(INR)"].sum()
    daily_cost.plot(kind="line", marker="o", color="#52ab98", ax=ax)
    ax.set_title("Daily Energy Cost Trend")
    ax.set_xlabel("Date")
    ax.set_ylabel("Cost (INR)")
    plt.xticks(rotation=45)
    return fig


# ------------------------------------------------
# Room-wise Usage
# ------------------------------------------------
def plot_room_wise_usage(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    df.groupby("Room")["Usage_kWh"].sum().plot(kind="bar", color="#1f4e5f", ax=ax)
    ax.set_title("Room-wise Energy Usage")
    ax.set_xlabel("Room")
    ax.set_ylabel("Usage (kWh)")
    plt.xticks(rotation=45)
    return fig
