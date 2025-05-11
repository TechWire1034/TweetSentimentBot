from dotenv import load_dotenv
import os
import tweepy

load_dotenv()
bearer_token = os.getenv("BEARER_TOKEN")

class SentimentStream(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        print(f"Tweet: {tweet.text}")
    def on_error(self, status):
        print(f"Error: {status}")
    def on_exception(self, exception):
        print(f"Exception: {exception}")

try:
    stream = SentimentStream(bearer_token=bearer_token)
    stream.add_rules(tweepy.StreamRule("python"))  # Simplified rule
    stream.filter()
except tweepy.TweepyException as e:
    print(f"Error: {e}")
