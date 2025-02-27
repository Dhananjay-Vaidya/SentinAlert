import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd

# Download necessary NLP data
nltk.download("stopwords")
nltk.download("wordnet")

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    if not isinstance(text, str):
        return ""

    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)  # Remove URLs
    text = re.sub(r"@\w+", lambda x: x.group(0)[1:], text)  # Keep mentions without '@'
    text = re.sub(r"#\w+", lambda x: x.group(0)[1:], text)  # Keep hashtags without '#'
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # Remove non-alphabetic characters
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return " ".join(words).strip()

def preprocess_data(google_news_data, social_searcher_data):
    # Convert JSON data to Pandas DataFrame
    google_news_df = pd.DataFrame(google_news_data)
    social_searcher_df = pd.DataFrame(social_searcher_data)

    # Apply text cleaning
    google_news_df['cleaned_text'] = google_news_df['description'].apply(clean_text)
    social_searcher_df['cleaned_text'] = social_searcher_df['text'].apply(clean_text)

    return google_news_df, social_searcher_df
