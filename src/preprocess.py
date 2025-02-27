import os
import json
import pandas as pd

# Get the absolute path for the data directory
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

def preprocess_google_news():
    input_file = os.path.join(DATA_DIR, 'google_news_data.json')
    output_file = os.path.join(DATA_DIR, 'google_news_processed_data.csv')
    
    if not os.path.exists(input_file):
        print(f"Google News data file not found: {input_file}")
        return
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'articles' not in data:
            print("Invalid Google News data format.")
            return
        
        df = pd.json_normalize(data['articles'])

        # Select and rename relevant columns
        df = df[['title', 'description', 'publishedAt', 'source.name', 'url']].fillna("")
        df.columns = ['title', 'description', 'timestamp', 'source', 'url']
        
        # Save to CSV
        df.to_csv(output_file, index=False)
        print(f"Processed Google News data saved to: {output_file}")

    except Exception as e:
        print(f"Error processing Google News data: {str(e)}")

def preprocess_social_searcher():
    input_file = os.path.join(DATA_DIR, 'social_searcher_data.json')
    output_file = os.path.join(DATA_DIR, 'social_searcher_processed_data.csv')
    
    if not os.path.exists(input_file):
        print(f"Social Searcher data file not found: {input_file}")
        return
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'posts' not in data:
            print("Invalid Social Searcher data format.")
            return
        
        df = pd.json_normalize(data['posts'])

        # Select and rename relevant columns
        df = df[['title', 'text', 'sentiment', 'image', 'url', 'user.name', 'posted']].fillna("")
        df.columns = ['title', 'text', 'sentiment', 'image', 'url', 'source', 'timestamp']
        
        # Save to CSV
        df.to_csv(output_file, index=False)
        print(f"Processed Social Searcher data saved to: {output_file}")

    except Exception as e:
        print(f"Error processing Social Searcher data: {str(e)}")

if __name__ == "__main__":
    preprocess_google_news()
    preprocess_social_searcher()
