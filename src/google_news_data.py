import requests
import json
import os
from config.configuration import GOOGLE_NEWS_API_KEY  

def get_google_news_data(query):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={GOOGLE_NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    # Check if the response is valid
    if data.get('status') != 'ok':
        print("Error fetching Google News data.")
        return

    # Set data directory relative to your project
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
    os.makedirs(data_dir, exist_ok=True)
    
    # Save data to json file in the project data folder
    file_path = os.path.join(data_dir, 'google_news_data.json')
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"Google News data saved to {file_path}")

if __name__ == "__main__":
    get_google_news_data("technology")
