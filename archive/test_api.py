from dotenv import load_dotenv
import os
import tweepy
import time

load_dotenv()
bearer_token = os.getenv("BEARER_TOKEN")
client = tweepy.Client(bearer_token=bearer_token)

try:
    query = "#Python -is:retweet lang:en"
    tweets = client.search_recent_tweets(query=query, max_results=10)
    for tweet in tweets.data:
        print(f"Tweet: {tweet.text}")
except tweepy.TooManyRequests as e:
    reset_time = int(e.response.headers.get("x-rate-limit-reset", 0))
    wait_seconds = reset_time - int(time.time()) + 1 if reset_time else 900
    print(f"Rate limit exceeded. Waiting {wait_seconds} seconds...")
    time.sleep(wait_seconds)
except Exception as e:
    print(f"Error: {e}")