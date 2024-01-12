import os

from dotenv import load_dotenv

load_dotenv()

TWITTER_CONSUMER_KEY = os.environ["TWITTER_CONSUMER_KEY"]
TWITTER_CONSUMER_SECRET = os.environ["TWITTER_CONSUMER_SECRET"]
TWITTER_ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
TWITTER_ACCESS_SECRET = os.environ["TWITTER_ACCESS_SECRET"]

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
HUGGINGFACE_API_KEY = os.environ["HUGGINGFACE_API_KEY"]

OPENWEATHER_API_KEY = os.environ["OPENWEATHER_API_KEY"]

REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = os.environ["REDIS_PORT"]
# REDIS_PASSWORD = os.environ["REDIS_PASSWORD"]

MONGODB_URL = os.environ["MONGODB_URL"]
