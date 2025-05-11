import tweepy
from transformers import pipeline
import matplotlib.pyplot as plt
import argparse
import re
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
bearer_token = os.getenv("BEARER_TOKEN")

# Argument parser for tracking keyword
parser = argparse.ArgumentParser(description="Tweet Sentiment Bot")
parser.add_argument("--track", required=True, help="Keyword to track (e.g., #Python)")
args = parser.parse_args()

# Clean tweet text
def clean_text(text):
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()

# Sentiment analysis setup
sentiment_analyzer = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")
sentiment_data = {"positive": 0, "negative": 0, "neutral": 0}

# Tweet streaming (using polling as a fallback)
client = tweepy.Client(bearer_token=bearer_token)
query = f"{args.track} -is:retweet"
tweets = client.search_recent_tweets(query=query, max_results=10)

# Process tweets
for tweet in tweets.data:
    cleaned_text = clean_text(tweet.text)
    if cleaned_text:
        sentiment = sentiment_analyzer(cleaned_text)[0]
        label = sentiment['label'].lower()
        if "positive" in label:
            sentiment_data["positive"] += 1
        elif "negative" in label:
            sentiment_data["negative"] += 1
        else:
            sentiment_data["neutral"] += 1
        print(f"Tweet: {tweet.text} | Sentiment: {label} ({sentiment['score']:.2f})")

# Visualize results
total = sum(sentiment_data.values())
labels = list(sentiment_data.keys())
values = [v/total*100 for v in sentiment_data.values()]
plt.bar(labels, values, color=['green', 'red', 'blue'])
plt.title(f"Sentiment Insights: {args.track} Tweets")
plt.ylabel("Percentage")
plt.show()

print(f"Sentiment Distribution: {sentiment_data} | Total: {total}")
