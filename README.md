Sentiment Analysis and Alert System


![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Streamlit](https://img.shields.io/badge/streamlit-app-red)
![Last Commit](https://img.shields.io/github/last-commit/Dhananjay-Vaidya/SentinAlert)
![Issues](https://img.shields.io/github/issues/Dhananjay-Vaidya/SentinAlert)
![Forks](https://img.shields.io/github/forks/Dhananjay-Vaidya/SentinAlert?style=social)
![Stars](https://img.shields.io/github/stars/Dhananjay-Vaidya/SentinAlert?style=social)
![Contributions](https://img.shields.io/badge/contributions-welcome-blue)
![Build](https://img.shields.io/badge/build-passing-brightgreen)


Table of Contents :s

Project Description
Motivation
Problem Statement
Technologies Used
Current Features
Installation
Usage
Dataset
Contributing
Author
License


Project Description

The Sentiment Analysis and Alert System is a real-time monitoring application that collects news and social media data, analyzes sentiment, and generates alerts based on the detected sentiment. The system leverages TextBlob for sentiment analysis and provides a Streamlit dashboard for visualizing real-time insights.


Motivation

With the increasing flow of information online, businesses, organizations, and governments need to monitor real-time sentiments in news and social media. This project enables automatic tracking of sentiment trends, helping users take proactive actions based on the sentiment detected.


Problem Statement

The goal of this project is to develop a system that:

Collects news and social media data in real-time
Performs sentiment analysis to classify data as Positive, Neutral, or Negative
Generates alerts based on sentiment scores
Displays results on an interactive Streamlit dashboard


Technologies Used

This project is built using the following technologies:

Python – Core programming language
Google News API – Fetches real-time news data
Social Searcher API – Collects social media sentiment data
TextBlob – Performs sentiment analysis
Pandas & NumPy – Data handling and preprocessing
Matplotlib & Seaborn – Data visualization
Streamlit – Interactive web-based dashboard
Joblib – Saves and loads models efficiently


Installation

To install and set up the project, follow these steps:

1️⃣ Clone the Repositor :
git clone https://https://github.com/Dhananjay-Vaidya/SentinAlert.git
cd sentiment-alert-system

2️⃣ Create a Virtual Environment :
python -m venv venv
source venv/bin/activate  
# On Windows: venv\Scripts\activate

3️⃣ Install Dependencie
pip install -r requirements.txt


Usage

1️⃣ Run Sentiment Analysis & Alert :
python src/sentiment_alert.py

2️⃣ Launch the Streamlit Dashboar
streamlit run app/streamlit_app.py
This will open an interactive dashboard where you can view real-time sentiment trends and alerts.


Dataset
The project does not rely on a static dataset but collects real-time data using Google News API and Social Searcher API. The collected data is preprocessed and stored in:

data/processed_google_news_data.json
data/processed_social_media_data.json


License
This project is licensed under the MIT License. See the LICENSE file for details.