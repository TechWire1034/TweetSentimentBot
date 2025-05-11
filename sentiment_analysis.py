from transformers import pipeline
import re

# Initialize sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

# Clean tweet text, preserve hashtags
def clean_text(text):
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)  # Remove URLs
    text = re.sub(r'@\w+', '', text)  # Remove mentions
    text = re.sub(r'[^\w\s#]', '', text)  # Keep hashtags, remove other special chars
    return text.strip()

# Analyze tweets
def analyze_tweets():
    input_file = r"C:\Users\Unknown01\Desktop\Grok\tweets.txt"
    output_file = r"C:\Users\Unknown01\Desktop\Grok\sentiment_results.txt"
    sentiment_data = {"positive": 0, "negative": 0, "neutral": 0}
    lines_processed = 0

    with open(input_file, 'r', encoding='utf-8') as f, open(output_file, 'w', encoding='utf-8') as out:
        for line in f:
            tweet_text = line.strip()
            if lines_processed < 50:  # Limit to 50 lines
                if tweet_text:
                    cleaned_text = clean_text(tweet_text)
                    if cleaned_text:
                        result = sentiment_analyzer(cleaned_text)[0]
                        sentiment = {"LABEL_0": "negative", "LABEL_1": "neutral", "LABEL_2": "positive"}[result['label']]
                        score = result['score']
                        sentiment_data[sentiment] += 1
                        out.write(f"Tweet: {tweet_text}\nSentiment: {sentiment} (Score: {score:.2f})\n\n")
                        print(f"Tweet: {tweet_text}\nSentiment: {sentiment} (Score: {score:.2f})\n")
                    else:
                        print(f"Skipped empty cleaned tweet: {tweet_text}")
                lines_processed += 1

    total = sum(sentiment_data.values())
    print(f"Sentiment Distribution: {sentiment_data} | Total: {total} (Processed {lines_processed} lines)")

if __name__ == "__main__":
    analyze_tweets()
