import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from transformers import pipeline
from sklearn.ensemble import IsolationForest
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

# Define constants
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
EMAIL_ALERTS = True  # Enable email alerts

# Load sentiment analysis model
sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", revision="main")

# Dark Mode Toggle
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Function for sentiment analysis
def analyze_sentiment(text):
    if not isinstance(text, str):
        return {"sentiment": "Neutral", "score": 0}

    result = sentiment_model(text)[0]
    return {"sentiment": result['label'], "score": result['score']}

# Load and process data
def load_and_process_data(source):
    file_path = os.path.join(DATA_DIR, f'{source}_processed_data.csv')
    if not os.path.exists(file_path):
        st.error(f"Data file not found: {file_path}")
        return None

    df = pd.read_csv(file_path)
    # Fix timestamp column selection dynamically
    if source == 'google_news':
        date_column = 'publishedAt' if 'publishedAt' in df.columns else 'timestamp'
    else:  # social_searcher
        date_column = 'posted' if 'posted' in df.columns else 'timestamp'

    # Ensure column exists before assignment
    if date_column in df.columns:
        df['timestamp'] = pd.to_datetime(df[date_column], errors='coerce')
    else:
        st.error(f"⚠️ Error: Column '{date_column}' not found in {source} dataset.")
        return None

    # Ensure text column selection
    if 'description' in df.columns:
        df['text'] = df['title'] + ' ' + df['description'].fillna('')
    elif 'text' in df.columns:
        df['text'] = df['text'].fillna('')
    else:
        st.error(f"⚠️ Error: No valid text column found in {source} dataset.")
        return None

    df['source'] = source.title().replace('_', ' ')

    with st.spinner("🔄 Analyzing sentiment..."):
        sentiment_data = df['text'].apply(analyze_sentiment)

    df['sentiment'] = sentiment_data.apply(lambda x: x['sentiment'])
    df['sentiment_score'] = sentiment_data.apply(lambda x: x['score'])

    return df

# Anomaly Detection
def detect_anomalies(df):
    if len(df) < 10:
        return []

    model = IsolationForest(contamination=0.05, random_state=42)
    # Ensure column names are used
    X = df[['sentiment_score']].copy()
    X.columns = ['sentiment_score']  # Assign correct column names

    df['anomaly'] = model.fit_predict(X)
    return df[df['anomaly'] == -1]

# Email alert function
def send_email_alert(subject, message):
    if not EMAIL_ALERTS:
        return

    sender_email = "your_email@example.com"
    receiver_email = "alert_recipient@example.com"
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login(sender_email, "your_password")
            server.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception as e:
        st.error(f"Failed to send alert email: {str(e)}")

# UI Layout
def main():
    st.set_page_config(page_title="Sentiment Analysis Dashboard", layout="wide")

    # Sidebar Controls
    with st.sidebar:
        st.title("⚙️ Controls")
        
        # Dark Mode Toggle
        dark_mode_toggle = st.sidebar.checkbox("🌙 Dark Mode", value=st.session_state.dark_mode)

        if dark_mode_toggle:
            st.session_state.dark_mode = True
            dark_style = """
                <style>
                body, .stApp {
                    background-color: #222222;
                    color: white;
                }
                h1, h2, h3, h4, h5, h6, p, label, .stTextInput, .stSelectbox, .stCheckbox, .stRadio, .stButton {
                    color: white !important;
                }
                .stDataFrame, .stPlotlyChart {
                    background-color: #333333;
                }
                .css-1aumxhk {
                    background-color: #444444 !important;
                }
                </style>
            """
        else:
            st.session_state.dark_mode = False
            dark_style = ""  # Reset styles if Dark Mode is off

        st.markdown(dark_style, unsafe_allow_html=True)

        # Data Source Selector
        data_source = st.radio("📡 Select Data Source", ["social_searcher", "google_news"])

        # Date Range Selector
        date_range = st.date_input("📅 Select Date Range", [])

        # Keyword Filter
        keyword_filter = st.text_input("🔍 Search Keyword")

    st.title("🚀 AI-Powered Sentiment Analysis Dashboard")

    # Load Data
    df = load_and_process_data(data_source)

    if df is not None and not df.empty:
        # Filter by Date
        if date_range:
            df = df[(df['timestamp'].dt.date >= date_range[0]) & (df['timestamp'].dt.date <= date_range[1])]

        # Filter by Keyword
        if keyword_filter:
            df = df[df['text'].str.contains(keyword_filter, case=False, na=False)]

        # Detect Anomalies
        anomalies = detect_anomalies(df)
        if not anomalies.empty:
            st.error("🚨 Anomalous Sentiment Detected!")
            send_email_alert("Sentiment Alert", "Unusual sentiment trend detected!")

        # Layout
        col1, col2 = st.columns(2)

        # 📊 Sentiment Trends
        with col1:
            st.subheader("📊 Sentiment Trends Over Time")
            fig = go.Figure()
            for source in df['source'].unique():
                source_data = df[df['source'] == source]
                fig.add_trace(go.Scatter(
                    x=source_data['timestamp'],
                    y=source_data['sentiment_score'].rolling(window=5).mean(),
                    mode='lines+markers',
                    name=source
                ))
            fig.update_layout(title='Sentiment Over Time', xaxis_title='Date', yaxis_title='Sentiment Score')
            st.plotly_chart(fig, use_container_width=True)

        # 🔎 Sentiment Distribution
        with col2:
            st.subheader("🔎 Sentiment Distribution")
            sentiment_counts = df['sentiment'].value_counts()
            pie_chart = px.pie(values=sentiment_counts.values, names=sentiment_counts.index, title='Sentiment Breakdown')
            st.plotly_chart(pie_chart, use_container_width=True)

        # 📌 Sentiment Score Gauge
        avg_sentiment_score = df['sentiment_score'].mean()
        st.subheader("📌 Sentiment Score Gauge")
        gauge_fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_sentiment_score,
            title={"text": "Average Sentiment Score"},
            gauge={"axis": {"range": [0, 1]}}
        ))
        st.plotly_chart(gauge_fig, use_container_width=True)

        # 📝 Recent Posts
        st.subheader("📝 Recent Posts")
        st.dataframe(df[['timestamp', 'text', 'sentiment', 'sentiment_score', 'source']].sort_values('timestamp', ascending=False).head(10))

    else:
        st.error("❌ No data available. Please check your data files.")

if __name__ == "__main__":
    main()