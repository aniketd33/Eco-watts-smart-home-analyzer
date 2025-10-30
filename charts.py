import plotly.express as px
import pandas as pd

# -----------------------------------------------------
# 📊 Appliance-wise Energy Usage Chart
# -----------------------------------------------------
def plot_usage_by_appliance(df):
    try:
        fig = px.bar(
            df.groupby("appliance")["Usage_kWh"].sum().reset_index(),
            x="appliance",
            y="Usage_kWh",
            color="appliance",
            title="🔌 Energy Usage by Appliance",
            text_auto=".2f",
            template="plotly_white",
        )
        fig.update_layout(
            title_x=0.3,
            showlegend=False,
            xaxis_title="Appliance",
            yaxis_title="Energy Usage (kWh)",
            font=dict(family="Poppins", size=14, color="#2d6a4f"),
            plot_bgcolor="rgba(0,0,0,0)",
        )
        return fig
    except Exception as e:
        raise Exception(f"Error in plot_usage_by_appliance: {e}")

# -----------------------------------------------------
# 💰 Daily Energy Cost Trend
# -----------------------------------------------------
def plot_daily_cost_trend(df):
    try:
        df["Date"] = pd.to_datetime(df["Timestamp"]).dt.date
        daily_cost = df.groupby("Date")["Cost(INR)"].sum().reset_index()

        fig = px.line(
            daily_cost,
            x="Date",
            y="Cost(INR)",
            markers=True,
            title="📆 Daily Energy Cost Trend",
            template="plotly_white",
            line_shape="spline"
        )
        fig.update_traces(line_color="#1b4332", line_width=3)
        fig.update_layout(
            xaxis=dict(showgrid=False, tickangle=-45),
            yaxis_title="Cost (INR)",
            font=dict(family="Poppins", size=14, color="#1b4332"),
            plot_bgcolor="rgba(0,0,0,0)"
        )
        return fig
    except Exception as e:
        raise Exception(f"Error in plot_daily_cost_trend: {e}")

# -----------------------------------------------------
# 🏠 Room-wise Energy Usage (Compact)
# -----------------------------------------------------
def plot_room_wise_usage(df):
    try:
        room_usage = df.groupby("Room")["Usage_kWh"].sum().reset_index()
        fig = px.pie(
            room_usage,
            names="Room",
            values="Usage_kWh",
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Greens_r,
            title="🏠 Room-wise Energy Usage"
        )
        fig.update_traces(textinfo="percent+label", textfont_size=14)
        fig.update_layout(
            title_x=0.3,
            font=dict(family="Poppins", size=14, color="#2d6a4f"),
            showlegend=True
        )
        return fig
    except Exception as e:
        raise Exception(f"Error in plot_room_wise_usage: {e}")


