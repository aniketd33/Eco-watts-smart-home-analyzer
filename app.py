import streamlit as st
import pandas as pd
from charts import plot_usage_by_appliance, plot_daily_cost_trend, plot_room_wise_usage

# ----------------------------
# ⚡ SMART HOME ENERGY ANALYZER (EcoWatts)
# ----------------------------
st.set_page_config(
    page_title="EcoWatts Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# Dashboard Title and Description
# ----------------------------
st.markdown(
    """
    <style>
    .big-font {
        font-size:32px !important;
        font-weight:700;
        color:#1E88E5;
    }
    .small-font {
        font-size:18px !important;
        color:#555;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<p class="big-font">⚡ EcoWatts – Smart Home Energy Analyzer</p>', unsafe_allow_html=True)
st.markdown('<p class="small-font">Gain insights into electricity usage, cost trends, and room-wise consumption to promote energy efficiency.</p>', unsafe_allow_html=True)
st.markdown("---")

# ----------------------------
# Upload CSV Section
# ----------------------------
with st.sidebar:
    st.header("📂 Upload Dataset")
    uploaded_file = st.file_uploader("Upload your energy usage CSV file", type=["csv"])
    st.markdown("---")
    st.markdown("💡 **Tip:** Use your household energy log file or download a demo dataset to test the dashboard.")

# ----------------------------
# Load and Display Data
# ----------------------------
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Convert timestamp column
    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    st.success("✅ Data uploaded successfully!")
    st.dataframe(df.head())

    # ----------------------------
    # Visual Insights Section
    # ----------------------------
    st.subheader("📊 Visual Insights")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🔌 Appliance-wise Energy Usage")
        fig1 = plot_usage_by_appliance(df)
        st.pyplot(fig1, use_container_width=True)

    with col2:
        st.markdown("#### 💰 Daily Energy Cost Trend")
        fig2 = plot_daily_cost_trend(df)
        st.pyplot(fig2, use_container_width=True)

    # ----------------------------
    # Room-wise Energy Usage
    # ----------------------------
    st.markdown("---")
    st.subheader("🏠 Room-wise Energy Usage")
    try:
        fig3 = plot_room_wise_usage(df)
        st.pyplot(fig3, use_container_width=True)
    except Exception as e:
        st.warning(f"⚠️ Unable to load Room-wise chart: {e}")

    # ----------------------------
    # Insights Section
    # ----------------------------
    st.markdown("---")
    st.subheader("💡 Insights Summary")
    st.info("""
    - High consumption appliances highlight optimization opportunities.  
    - The **Daily Cost Trend** helps track electricity spending habits.  
    - **Room-wise Usage** reveals the most energy-intensive areas in your home.  
    - Can be integrated with **IoT sensors** for real-time analytics.
    """)

else:
    st.warning("👆 Please upload a CSV file to begin analysis.")

# ----------------------------
# Footer Section
# ----------------------------
st.markdown("---")
st.markdown(
    """
    <div style='text-align:center; font-size:16px; color:gray;'>
    👨‍💻 <b>Author:</b> Aniket Dombale <br>
    © 2025 | EcoWatts Smart Home Energy Analyzer | Open Source Project
    </div>
    """,
    unsafe_allow_html=True
)


