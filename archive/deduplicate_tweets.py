# deduplicate_tweets.py
input_file = r"C:\Users\Unknown01\Desktop\Grok\tweets.txt"
output_file = r"C:\Users\Unknown01\Desktop\Grok\tweets_cleaned.txt"

unique_tweets = []
with open(input_file, 'r', encoding='utf-8') as f:
    for line in f:
        tweet = line.strip()
        if tweet and tweet not in unique_tweets:
            unique_tweets.append(tweet)

with open(output_file, 'w', encoding='utf-8') as f:
    for tweet in unique_tweets[:50]:  # Keep only 50 tweets
        f.write(f"{tweet}\n")

print(f"Cleaned {len(unique_tweets)} unique tweets, saved 50 to {output_file}")
