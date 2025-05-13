from transformers import pipeline
import re
import os

print("Starting sentiment_analysis.py...")

try:
    # Initialize sentiment analysis pipeline
    try:
        sentiment_analyzer = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")
        print("Sentiment analysis model loaded successfully.")
    except Exception as e:
        print(f"Error loading sentiment analysis model: {e}")
        exit(1)

    # Clean tweet text, preserve hashtags
    def clean_text(text):
        try:
            text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)  # Remove URLs
            text = re.sub(r'@\w+', '', text)  # Remove mentions
            text = re.sub(r'[^\w\s#]', '', text)  # Keep hashtags, remove other special chars
            return text.strip()
        except Exception as e:
            print(f"Error cleaning text: {e}")
            return ""

    # Analyze tweets
    def analyze_tweets():
        input_file = r"C:\Users\Unknown01\Desktop\Grok\tweets.txt"
        output_file = r"C:\Users\Unknown01\Desktop\Grok\sentiment_results.txt"
        sentiment_data = {"positive": 0, "negative": 0, "neutral": 0}
        lines_processed = 0

        try:
            if not os.path.exists(input_file):
                raise FileNotFoundError(f"{input_file} does not exist.")
            with open(input_file, 'r', encoding='utf-8') as f, open(output_file, 'w', encoding='utf-8') as out:
                print(f"Opened {input_file} for reading and {output_file} for writing.")
                for line in f:
                    tweet_text = line.strip()
                    if lines_processed < 50:  # Limit to 50 lines
                        if tweet_text:
                            cleaned_text = clean_text(tweet_text)
                            if cleaned_text:
                                try:
                                    result = sentiment_analyzer(cleaned_text)[0]
                                    sentiment = {"LABEL_0": "negative", "LABEL_1": "neutral", "LABEL_2": "positive"}[result['label']]
                                    score = result['score']
                                    sentiment_data[sentiment] += 1
                                    out.write(f"Tweet: {tweet_text}\nSentiment: {sentiment} (Score: {score:.2f})\n\n")
                                    print(f"Tweet: {tweet_text}\nSentiment: {sentiment} (Score: {score:.2f})\n")
                                except Exception as e:
                                    print(f"Error analyzing tweet: {e}")
                            else:
                                print(f"Skipped empty cleaned tweet: {tweet_text}")
                            lines_processed += 1
                        else:
                            print("Skipped empty line.")
                    else:
                        break

            total = sum(sentiment_data.values())
            if total == 0:
                print("Warning: No tweets were analyzed successfully.")
            else:
                print(f"Sentiment Distribution: {sentiment_data} | Total: {total} (Processed {lines_processed} lines)")

        except FileNotFoundError as e:
            print(f"Error: {e}. Ensure {input_file} exists.")
            exit(1)
        except IOError as e:
            print(f"Error accessing files: {e}")
            exit(1)

    if __name__ == "__main__":
        analyze_tweets()

except Exception as e:
    print(f"Unexpected error in sentiment_analysis.py: {e}")
    exit(1)