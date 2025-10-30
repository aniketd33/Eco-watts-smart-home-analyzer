import plotly.express as px
import pandas as pd

# ----------------------------------------------
# ⚡ Chart 1: Energy Usage by Appliance
# ----------------------------------------------
def plot_usage_by_appliance(df):
    """
    Plots total energy usage grouped by appliance.
    """
    if 'Appliance' not in df.columns or 'Usage_kWh' not in df.columns:
        raise ValueError("Dataset must include 'Appliance' and 'Usage_kWh' columns.")

    usage_data = df.groupby('Appliance')['Usage_kWh'].sum().reset_index()
    fig = px.bar(
        usage_data,
        x='Appliance',
        y='Usage_kWh',
        text='Usage_kWh',
        color='Appliance',
        color_discrete_sequence=px.colors.sequential.Greens_r,
        title='🔌 Energy Usage by Appliance',
        template='plotly_white'
    )
    fig.update_traces(texttemplate='%{text:.2f} kWh', textposition='outside')
    fig.update_layout(
        xaxis_title='Appliance',
        yaxis_title='Total Usage (kWh)',
        showlegend=False,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    return fig


# ----------------------------------------------
# ⚡ Chart 2: Daily Energy Cost Trend
# ----------------------------------------------
def plot_daily_cost_trend(df):
    """
    Shows total daily electricity cost trend using line + markers.
    """
    if 'Timestamp' not in df.columns or 'Cost(INR)' not in df.columns:
        raise ValueError("Dataset must include 'Timestamp' and 'Cost(INR)' columns.")

    df['Date'] = pd.to_datetime(df['Timestamp']).dt.date
    daily_cost = df.groupby('Date')['Cost(INR)'].sum().reset_index()

    fig = px.line(
        daily_cost,
        x='Date',
        y='Cost(INR)',
        markers=True,
        title='📅 Daily Energy Cost Trend',
        template='plotly_white',
        color_discrete_sequence=['#2E8B57']
    )
    fig.update_traces(line=dict(width=3))
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Total Cost (₹)',
        margin=dict(l=20, r=20, t=60, b=40),
        xaxis_tickangle=-45
    )
    return fig


# ----------------------------------------------
# ⚡ Chart 3: Room-wise Energy Usage Distribution
# ----------------------------------------------
def plot_room_wise_usage(df):
    """
    Displays the percentage of energy consumption per room (pie chart).
    """
    if 'Room' not in df.columns or 'Usage_kWh' not in df.columns:
        raise ValueError("Dataset must include 'Room' and 'Usage_kWh' columns.")

    room_usage = df.groupby('Room')['Usage_kWh'].sum().reset_index()
    fig = px.pie(
        room_usage,
        names='Room',
        values='Usage_kWh',
        title='🏠 Room-wise Energy Usage Distribution',
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Aggrnyl
    )
    fig.update_layout(
        showlegend=True,
        legend_title_text='Rooms',
        margin=dict(l=40, r=40, t=60, b=40)
    )
    return fig


