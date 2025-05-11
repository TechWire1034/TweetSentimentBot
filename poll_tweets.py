from dotenv import load_dotenv
import os
import tweepy
import time
from datetime import datetime

load_dotenv()
bearer_token = os.getenv("BEARER_TOKEN")
client = tweepy.Client(bearer_token=bearer_token)

since_id = None
tweet_count = 0
max_tweets = 50

try:
    with open("tweets.txt", "w", encoding="utf-8") as f:
        while True:
            if tweet_count >= max_tweets:
                print(f"Collected {tweet_count} tweets. Stopping polling.")
                break
            try:
                query = "#Python OR #Coding -is:retweet"
                tweets = client.search_recent_tweets(query=query, max_results=10, since_id=since_id)
                if tweets.data:
                    for tweet in tweets.data:
                        tweet_text = f"Tweet: {tweet.text}\n"
                        print(tweet_text.strip())
                        f.write(tweet_text)
                        f.flush()
                        tweet_count += 1
                    since_id = tweets.data[0].id
                else:
                    print(f"No new tweets at {datetime.now()}")
                time.sleep(120)
            except tweepy.errors.TooManyRequests as e:
                print(f"Rate limit hit at {datetime.now()}. Waiting 15 minutes to retry...")
                wait_time = 900
                for i in range(wait_time, 0, -1):
                    minutes, seconds = divmod(i, 60)
                    print(f"Time remaining: {minutes:02d}:{seconds:02d}", end="\r")
                    time.sleep(1)
                print("\nResuming polling...")
            except tweepy.TweepyException as e:
                print(f"Error: {e}")
                time.sleep(120)
except IOError as e:
    print(f"File error: {e}. Ensure you have write permissions for tweets.txt.")
    raise
