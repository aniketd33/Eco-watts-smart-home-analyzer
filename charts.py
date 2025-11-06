import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")


# ---------------------------------
# 📊 Chart 1: Energy Usage by Appliance
# ---------------------------------
def plot_usage_by_appliance(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    usage = df.groupby("Appliance")["Usage_kWh"].sum().sort_values(ascending=False)
    sns.barplot(x=usage.values, y=usage.index, palette="Blues_d", ax=ax)
    ax.set_title("🔌 Energy Usage by Appliance", fontsize=13, fontweight="bold", color="#2b6777")
    ax.set_xlabel("Usage (kWh)")
    ax.set_ylabel("Appliance")
    plt.tight_layout()
    return fig


# ---------------------------------
# 📈 Chart 2: Daily Energy Cost Trend
# ---------------------------------
def plot_daily_cost_trend(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    df["Date"] = df["Timestamp"].dt.date
    daily_cost = df.groupby("Date")["Cost(INR)"].sum()

    sns.lineplot(x=daily_cost.index, y=daily_cost.values, color="#ffb703", marker="o", ax=ax)
    ax.set_title("📅 Daily Energy Cost Trend", fontsize=13, fontweight="bold", color="#2b6777")
    ax.set_xlabel("Date")
    ax.set_ylabel("Cost (INR)")
    ax.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    return fig


# ---------------------------------
# 🏠 Chart 3: Room-wise Energy Usage
# ---------------------------------
def plot_room_wise_usage(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    if "Room" in df.columns:
        room_usage = df.groupby("Room")["Usage_kWh"].sum().sort_values(ascending=False)
        colors = sns.color_palette("YlGnBu", len(room_usage))
        sns.barplot(x=room_usage.index, y=room_usage.values, palette=colors, ax=ax)
        ax.set_title("🏠 Room-wise Energy Usage", fontsize=13, fontweight="bold", color="#2b6777")
        ax.set_xlabel("Room")
        ax.set_ylabel("Total Usage (kWh)")
        plt.xticks(rotation=30)
    else:
        ax.text(0.3, 0.5, "Room column not found in dataset", fontsize=12, color="red")
    plt.tight_layout()
    return fig


