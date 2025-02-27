import os
from dotenv import load_dotenv

load_dotenv()

SOCIAL_SEARCHER_API_KEY = os.getenv("SOCIAL_SEARCHER_API_KEY")
GOOGLE_NEWS_API_KEY = os.getenv("GOOGLE_NEWS_API_KEY")

DATA_PATH = "data/"
