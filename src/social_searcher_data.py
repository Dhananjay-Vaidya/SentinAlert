import requests
import json
import os
from config.configuration import SOCIAL_SEARCHER_API_KEY  

def get_social_searcher_data(query):
    url = f"https://api.social-searcher.com/v2/search?q={query}&key={SOCIAL_SEARCHER_API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    # Set data directory relative to your project
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
    os.makedirs(data_dir, exist_ok=True)
    
    # Save data to json file in the project data folder
    file_path = os.path.join(data_dir, 'social_searcher_data.json')
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"Social Searcher data saved to {file_path}")

if __name__ == "__main__":
    get_social_searcher_data("technology")
