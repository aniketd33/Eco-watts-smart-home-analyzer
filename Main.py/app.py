
import streamlit as st
import pandas as pd
from charts import plot_usage_by_appliance, plot_daily_cost_trend, plot_temp_vs_usage
from model import train_and_predict, load_and_preprocess

st.set_page_config(page_title='EcoWatts', layout='wide')

st.title('🌿 EcoWatts – Smart Home Energy Analyzer')
st.markdown('**A Streamlit app to visualize and predict home energy usage**')

with st.sidebar:
    st.header('Dataset')
    uploaded_file = st.file_uploader('Upload CSV', type=['csv'])
    use_sample = st.checkbox('Use sample dataset (uploaded dataset file)', value=True)
    st.markdown('---')
    st.header('Model')
    predict_periods = st.number_input('Days to predict (simple forecast)', min_value=1, max_value=30, value=7)
    st.markdown('---')

# Load data
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    sample_path = 'energy_usage_Dataset.csv'
    try:
        df = pd.read_csv(sample_path)
    except Exception as e:
        st.error(f'Could not load sample dataset at {sample_path}: {e}')
        st.stop()

# Basic preprocessing
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
st.subheader('Data Preview')
st.dataframe(df.head())

# Charts
st.subheader('Visualizations')
col1, col2 = st.columns(2)
with col1:
    fig1 = plot_usage_by_appliance(df)
    st.pyplot(fig1)
with col2:
    fig2 = plot_daily_cost_trend(df)
    st.pyplot(fig2)

st.subheader('Temperature vs Usage')
fig3 = plot_temp_vs_usage(df)
st.pyplot(fig3)

# Model training / prediction
st.subheader('Forecast (Linear Regression)')
X, y, df_daily = load_and_preprocess(df)
if st.button('Train model & predict'):
    pred_df, metrics = train_and_predict(X, y, periods=int(predict_periods), df_daily=df_daily)
    st.write('**Metrics:**')
    st.write(metrics)
    st.line_chart(pred_df.set_index('date')['predicted_usage'])
    st.table(pred_df.head(10))

st.markdown('---')
st.write('Prepared by: Aniket Dombale')
