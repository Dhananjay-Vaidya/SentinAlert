import logging
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Set up logging
def setup_logging():
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(log_dir, 'app.log')),
            logging.StreamHandler()
        ]
    )

# Helper function to load API keys from environment variables
def get_api_key(key_name):
    api_key = os.getenv(key_name)
    if not api_key:
        logging.error(f"API key for {key_name} not found.")
    return api_key

# Example of a general utility function for saving JSON data to a file
def save_to_json(data, file_path):
    import json
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        logging.info(f"Data saved to {file_path}")
    except Exception as e:
        logging.error(f"Failed to save data: {e}")
