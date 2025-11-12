import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="whitegrid")

def plot_usage_by_appliance(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    data = df.groupby("Appliance")["Usage_kWh"].sum().sort_values(ascending=False)
    sns.barplot(x=data.values, y=data.index, palette="crest", ax=ax)
    ax.set_title("🔌 Energy Usage by Appliance", fontsize=12, color="#2b6777", weight="bold")
    ax.set_xlabel("Total Usage (kWh)")
    ax.set_ylabel("Appliance")
    plt.tight_layout()
    return fig

def plot_daily_cost_trend(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    df["Date"] = df["Timestamp"].dt.date
    daily_cost = df.groupby("Date")["Cost(INR)"].sum()
    ax.plot(daily_cost.index, daily_cost.values, color="#52b788", marker="o", linewidth=2)
    ax.set_title("💰 Daily Energy Cost Trend", fontsize=12, color="#2b6777", weight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel("Cost (INR)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def plot_room_wise_usage(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    room_data = df.groupby("Room")["Usage_kWh"].sum().sort_values(ascending=False)
    colors = sns.color_palette("coolwarm", len(room_data))
    ax.bar(room_data.index, room_data.values, color=colors)
    ax.set_title("🏠 Room-wise Energy Usage", fontsize=12, color="#2b6777", weight="bold")
    ax.set_xlabel("Room")
    ax.set_ylabel("Usage (kWh)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig
