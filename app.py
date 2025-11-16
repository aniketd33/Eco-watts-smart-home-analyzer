# =====================================================================
# EcoWatt Smart Home Energy Analyzer (FINAL VERSION with CSS + 2–3 Month Forecast)
# =====================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression


# ----------------------------------------------------------
# Streamlit Config
# ----------------------------------------------------------
st.set_page_config(page_title="EcoWatt Smart Home Energy Analyzer", layout="wide")


# ----------------------------------------------------------
# Load Custom CSS
# ----------------------------------------------------------
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# ----------------------------------------------------------
# CSV Loader
# ----------------------------------------------------------
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)

    # Detect timestamp column
    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    else:
        for col in df.columns:
            if "date" in col.lower() or "time" in col.lower():
                df.rename(columns={col: "Timestamp"}, inplace=True)
                df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
                break

    return df


def to_csv(df):
    return df.to_csv(index=False).encode("utf-8")


# =====================================================================
# SIDEBAR
# =====================================================================
st.sidebar.title("EcoWatt Dashboard")

uploaded = st.sidebar.file_uploader("Upload Dataset", type=["csv"])
use_sample = st.sidebar.checkbox("Use Sample Dataset", True)

menu = st.sidebar.radio(
    "📌 Menu",
    [
        "🏠 Overview",
        "📊 Appliance Analytics",
        "🚪 Room Analytics",
        "🔮 Forecast",
        "💡 Smart Tips",
        "⬇️ Export"
    ]
)


# =====================================================================
# DATA LOADING
# =====================================================================
if uploaded:
    df = load_data(uploaded)
elif use_sample:
    df = load_data("Energy dataset.csv")
else:
    st.warning("Upload a dataset to continue.")
    st.stop()


# =====================================================================
# FIX COLUMN NAMES → Usage_KWh ONLY
# =====================================================================
df.columns = [c.strip() for c in df.columns]

rename_map = {
    "Usage_kWh": "Usage_KWh",
    "Usage_Kwh": "Usage_KWh",
    "usage_kwh": "Usage_KWh",
    "usage_KWh": "Usage_KWh"
}

df.rename(columns=rename_map, inplace=True)

if "Usage_KWh" not in df.columns:
    st.error("❌ ERROR: CSV must contain column `Usage_KWh`.")
    st.write("Detected columns:", df.columns.tolist())
    st.stop()


# =====================================================================
# MAIN TITLE
# =====================================================================
st.title("🌿 EcoWatt — Smart Home Energy Analyzer")


# =====================================================================
# 1️⃣ OVERVIEW PAGE
# =====================================================================
if menu == "🏠 Overview":

    st.subheader("Dataset Preview")
    st.dataframe(df.head(50))

    total_kwh = df["Usage_KWh"].sum()
    days = (df["Timestamp"].max() - df["Timestamp"].min()).days + 1
    avg_daily = total_kwh / days

    df_hourly = df.set_index("Timestamp").resample("H")["Usage_KWh"].sum().reset_index()
    peak_hour = df_hourly.loc[df_hourly["Usage_KWh"].idxmax(), "Timestamp"].hour

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Energy", f"{total_kwh:.2f} kWh")
    col2.metric("Avg Daily", f"{avg_daily:.2f} kWh")
    col3.metric("Peak Hour", f"{peak_hour}:00")
    col4.metric("Records", len(df))

    fig = px.line(df_hourly, x="Timestamp", y="Usage_KWh", title="Hourly Energy Trend")
    st.plotly_chart(fig, use_container_width=True)


# =====================================================================
# 2️⃣ APPLIANCE ANALYTICS
# =====================================================================
elif menu == "📊 Appliance Analytics":

    st.subheader("Total Appliance Consumption")

    app_tot = df.groupby("Appliance")["Usage_KWh"].sum().reset_index().sort_values("Usage_KWh", ascending=False)
    fig = px.bar(app_tot, x="Appliance", y="Usage_KWh", title="Appliance-wise Consumption")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Daily Trends Per Appliance")

    appliances = df["Appliance"].unique().tolist()
    sel = st.multiselect("Select Appliances", appliances, default=appliances[:3])

    if sel:
        df_sel = df[df["Appliance"].isin(sel)]
        df_sel = df_sel.groupby([pd.Grouper(key="Timestamp", freq="D"), "Appliance"])["Usage_KWh"].sum().reset_index()

        fig2 = px.line(df_sel, x="Timestamp", y="Usage_KWh", color="Appliance", title="Daily Trend")
        st.plotly_chart(fig2, use_container_width=True)


# =====================================================================
# 3️⃣ ROOM ANALYTICS
# =====================================================================
elif menu == "🚪 Room Analytics":

    st.subheader("Room-wise Energy Distribution")

    room_tot = df.groupby("Room")["Usage_KWh"].sum().reset_index()
    fig = px.pie(room_tot, names="Room", values="Usage_KWh", title="Room Share")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Heatmap — Hourly Consumption")

    df_h = df.set_index("Timestamp").resample("H")["Usage_KWh"].sum().reset_index()
    df_h["hour"] = df_h["Timestamp"].dt.hour
    df_h["dow"] = df_h["Timestamp"].dt.day_name()

    pivot = df_h.pivot_table(index="hour", columns="dow", values="Usage_KWh")

    fig2 = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale="Blues"
    ))
    fig2.update_layout(title="Heatmap: Hour vs Day")
    st.plotly_chart(fig2, use_container_width=True)


# =====================================================================
# 4️⃣ FORECAST — NEXT 2–3 MONTHS (DAILY)
# =====================================================================
elif menu == "🔮 Forecast":

    st.subheader("📅 Forecast — Next 2/3 Months (Daily Prediction)")

    # Daily data
    df_daily = df.set_index("Timestamp").resample("D")["Usage_KWh"].sum().reset_index()
    df_daily["day"] = df_daily["Timestamp"].dt.day
    df_daily["month"] = df_daily["Timestamp"].dt.month
    df_daily["year"] = df_daily["Timestamp"].dt.year
    df_daily["dow"] = df_daily["Timestamp"].dt.dayofweek
    df_daily["weekend"] = df_daily["dow"].isin([5,6]).astype(int)

    df_daily["lag_1"] = df_daily["Usage_KWh"].shift(1)
    df_daily["lag_7"] = df_daily["Usage_KWh"].shift(7)
    df_daily["lag_30"] = df_daily["Usage_KWh"].shift(30)
    df_daily["roll_7"] = df_daily["Usage_KWh"].rolling(7).mean()
    df_daily["roll_30"] = df_daily["Usage_KWh"].rolling(30).mean()

    df_daily = df_daily.dropna().reset_index(drop=True)

    FEATURES = ["day","month","year","dow","weekend","lag_1","lag_7","lag_30","roll_7","roll_30"]

    X = df_daily[FEATURES]
    y = df_daily["Usage_KWh"]

    model = LinearRegression()
    model.fit(X, y)

    months_to_predict = st.selectbox("Select Forecast Duration:", [2, 3], index=0)
    future_days = months_to_predict * 30

    temp = df_daily.copy()
    future_rows = []
    last_date = temp["Timestamp"].max()

    for i in range(future_days):

        next_date = last_date + pd.Timedelta(days=1)

        feat = {
            "day": next_date.day,
            "month": next_date.month,
            "year": next_date.year,
            "dow": next_date.dayofweek,
            "weekend": int(next_date.dayofweek in [5, 6]),
            "lag_1": temp.iloc[-1]["Usage_KWh"],
            "lag_7": temp.iloc[-7]["Usage_KWh"] if len(temp)>=7 else temp.iloc[-1]["Usage_KWh"],
            "lag_30": temp.iloc[-30]["Usage_KWh"] if len(temp)>=30 else temp.iloc[-1]["Usage_KWh"],
            "roll_7": temp["Usage_KWh"].tail(7).mean(),
            "roll_30": temp["Usage_KWh"].tail(30).mean()
        }

        pred = model.predict(pd.DataFrame([feat]))[0]

        future_rows.append({
            "Timestamp": next_date,
            "Forecast_KWh": float(np.round(pred, 3))
        })

        temp.loc[len(temp)] = [
            next_date,
            pred,
            next_date.day, next_date.month, next_date.year,
            next_date.dayofweek, feat["weekend"],
            feat["lag_1"], feat["lag_7"], feat["lag_30"],
            feat["roll_7"], feat["roll_30"]
        ]

        last_date = next_date

    future_df = pd.DataFrame(future_rows)

    st.success(f"Forecast generated for next {months_to_predict} months!")

    # Plot
    plot_actual = df_daily.tail(60).rename(columns={"Usage_KWh": "Value"})
    plot_forecast = future_df.rename(columns={"Forecast_KWh": "Value"})
    combined = pd.concat([plot_actual, plot_forecast])

    fig = px.line(combined, x="Timestamp", y="Value",
                  title=f"Last 60 Days + Next {months_to_predict} Months Forecast")
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(future_df)


# =====================================================================
# 5️⃣ SMART TIPS
# =====================================================================
elif menu == "💡 Smart Tips":

    st.subheader("AI Smart Tips")

    app_tot = df.groupby("Appliance")["Usage_KWh"].sum().reset_index()
    total = app_tot["Usage_KWh"].sum()

    tips = []

    for _, row in app_tot.sort_values("Usage_KWh", ascending=False).head(3).iterrows():
        pct = (row["Usage_KWh"] / total) * 100
        tips.append(f"⚡ {row['Appliance']} uses {pct:.1f}% — consider optimizing it.")

    if "Lights" in app_tot["Appliance"].values:
        lv = app_tot.loc[app_tot["Appliance"]=="Lights", "Usage_KWh"].values[0]
        if lv/total*100 > 5:
            tips.append("💡 Lights are consuming high power — use LEDs or sensors.")

    if "Refrigerator" in app_tot["Appliance"].values:
        rv = app_tot.loc[app_tot["Appliance"]=="Refrigerator","Usage_KWh"].values[0]
        if rv/total*100 > 20:
            tips.append("🧊 Fridge >20% — check seals & clean coils.")

    for t in tips:
        st.info(t)


# =====================================================================
# 6️⃣ EXPORT
# =====================================================================
elif menu == "⬇️ Export":

    st.subheader("Download Data")

    st.download_button("Download Raw CSV", to_csv(df), "raw_data.csv")

    hourly = df.set_index("Timestamp").resample("H")["Usage_KWh"].sum().reset_index()
    st.download_button("Download Hourly CSV", to_csv(hourly), "hourly_data.csv")

    st.success("Downloads ready!")

