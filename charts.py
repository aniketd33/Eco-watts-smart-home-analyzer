import plotly.express as px
import pandas as pd

def plot_usage_by_appliance(df):
    fig = px.pie(df, names='appliance', values='Usage_kWh',
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                 title="Appliance-wise Energy Usage")
    fig.update_traces(textinfo='percent+label')
    return fig


def plot_daily_cost_trend(df):
    df_daily = df.groupby(df["Timestamp"].dt.date)["Cost(INR)"].sum().reset_index()
    fig = px.line(df_daily, x="Timestamp", y="Cost(INR)", markers=True,
                  title="Daily Energy Cost Trend (INR)",
                  color_discrete_sequence=["#00796b"])
    fig.update_layout(xaxis_title="Date", yaxis_title="Total Cost (₹)")
    return fig


def plot_room_wise_usage(df):
    room_usage = df.groupby("Room")["Usage_kWh"].sum().reset_index()
    fig = px.bar(room_usage, x="Room", y="Usage_kWh",
                 color="Room", title="Room-wise Energy Usage",
                 color_discrete_sequence=px.colors.qualitative.Vivid)
    fig.update_layout(bargap=0.4)
    return fig


def plot_peak_usage_timeline(df):
    hourly_usage = df.groupby(df["Timestamp"].dt.hour)["Usage_kWh"].sum().reset_index()
    fig = px.bar(hourly_usage, x="Timestamp", y="Usage_kWh",
                 title="Peak Usage Hours in a Day",
                 color_discrete_sequence=["#004d40"])
    fig.update_layout(xaxis_title="Hour of Day", yaxis_title="Usage (kWh)")
    return fig



