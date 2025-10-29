import streamlit as st
import pandas as pd
from charts import plot_usage_by_appliance, plot_daily_cost_trend, plot_temp_vs_usage
from model import train_and_predict, load_and_preprocess

# -----------------------------------------------------------
# Streamlit App Configuration
# -----------------------------------------------------------
st.set_page_config(page_title='EcoWatts – Smart Home Energy Analyzer', layout='wide')

st.title('🌿 EcoWatts – Smart Home Energy Analyzer')
st.markdown('**A Streamlit app to visualize, analyze, and predict home energy usage**')

# -----------------------------------------------------------
# Sidebar – File Upload and Model Settings
# -----------------------------------------------------------
with st.sidebar:
    st.header('📂 Dataset')
    uploaded_file = st.file_uploader('Upload CSV file', type=['csv'])
    use_sample = st.checkbox('Use sample dataset (default)', value=True)
    st.markdown('---')

    st.header('⚙️ Model Settings')
    predict_periods = st.number_input('Days to predict (simple forecast)', min_value=1, max_value=30, value=7)
    st.markdown('---')

# -----------------------------------------------------------
# Load Dataset
# -----------------------------------------------------------
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    sample_path = 'energy_usage_Dataset.csv'
    try:
        df = pd.read_csv(sample_path)
    except Exception as e:
        st.error(f'❌ Could not load sample dataset: {e}')
        st.stop()

# -----------------------------------------------------------
# Data Preprocessing
# -----------------------------------------------------------
df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')

st.subheader('🧾 Data Preview')
st.dataframe(df.head())

# Detect flexible column names
usage_col = 'Usage_kWh' if 'Usage_kWh' in df.columns else 'Usage'
temp_col = 'Temp(C)' if 'Temp(C)' in df.columns else 'Temperature'

# -----------------------------------------------------------
# Visualizations
# -----------------------------------------------------------
st.subheader('📊 Visualizations')

col1, col2 = st.columns(2)

with col1:
    fig1 = plot_usage_by_appliance(df)
    st.pyplot(fig1)

with col2:
    fig2 = plot_daily_cost_trend(df)
    st.pyplot(fig2)

# Temperature vs Usage chart (fixed)
st.subheader('🌡️ Temperature vs Energy Usage')
try:
    fig3 = plot_temp_vs_usage(df, temp_col=temp_col, usage_col=usage_col)
    st.pyplot(fig3)
except Exception as e:
    st.warning(f"⚠️ Could not display Temperature vs Usage chart. Error: {e}")

# -----------------------------------------------------------
# Model Training & Prediction
# -----------------------------------------------------------
st.subheader('🤖 Forecast (Linear Regression)')
X, y, df_daily = load_and_preprocess(df)

if st.button('Train model & predict'):
    pred_df, metrics = train_and_predict(X, y, periods=int(predict_periods), df_daily=df_daily)
    st.write('**📈 Model Performance Metrics:**')
    st.write(metrics)
    st.line_chart(pred_df.set_index('date')['predicted_usage'])
    st.table(pred_df.head(10))

# -----------------------------------------------------------
# Footer
# -----------------------------------------------------------
st.markdown('---')
st.write('**👨‍💻 Author:** Aniket Dombale')
st.caption('EcoWatts Smart Home Energy Analyzer | © 2025 Open Source Project')

