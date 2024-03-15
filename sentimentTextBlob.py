import os
import json
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
from datetime import datetime

# load  data
with open('gatech_posts_with_comments.json') as file:
    data = json.load(file)

# funct to calculate TextBlob sentiment
def calculate_sentiment(text):
    return TextBlob(text).sentiment.polarity

# extract data from our json file
posts = []
for item in data:
    created_utc = datetime.utcfromtimestamp(item['created_utc']).strftime('%Y-%m-%d')
    post_score = item['score']
    post_sentiment = calculate_sentiment(item['title'] + '. ' + item['selftext'])
    posts.append({'type': 'post', 'text': item['title'], 'sentiment': post_sentiment, 'score': post_score, 'date': created_utc})

    for comment in item['comments']:
        comment_score = comment['score']
        comment_sentiment = calculate_sentiment(comment['body'])
        posts.append({'type': 'comment', 'text': comment['body'], 'sentiment': comment_sentiment, 'score': comment_score, 'date': created_utc})

df = pd.DataFrame(posts)


# Overall Sentiment
df['adjusted_sentiment'] = df['sentiment'] * df['score']
overall_sentiment = df['adjusted_sentiment'].mean()

# Sentiment Distribution plot
plt.figure()
df['sentiment'].hist(bins=20)
plt.title('TextBlob Sentiment Distribution')
plt.xlabel('Sentiment Score')
plt.ylabel('Frequency')
plt.savefig('results/TextBlob/textblob_sentiment_distribution.png')

# post vs comment Sentiment plot
plt.figure()
df.groupby('type')['sentiment'].mean().plot(kind='bar')
plt.title('Average TextBlob Sentiment: Post vs Comment')
plt.ylabel('Average Sentiment Score')
plt.savefig('results/TextBlob/post_vs_comment_sentiment.png')

# Temporal Trends
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)
plt.figure()
df.resample('M')['sentiment'].mean().plot()
plt.title('Monthly Sentiment Trends (TextBlob)')
plt.ylabel('Average Sentiment')
plt.savefig('results/TextBlob/monthly_sentiment_trends_textblob.png')

# sentiment Consistency
post_comment_sentiment = df.pivot_table(index='date', columns='type', values='sentiment', aggfunc='mean')
plt.figure()
post_comment_sentiment.plot()
plt.title('Post vs Comment Sentiment Over Time (TextBlob)')
plt.ylabel('Sentiment')
plt.savefig('results/TextBlob/post_comment_sentiment_over_time_textblob.png')

# we find most positive and negative texts
most_positive = df[df['sentiment'] == df['sentiment'].max()].iloc[0]
most_negative = df[df['sentiment'] == df['sentiment'].min()].iloc[0]


results = {
    "Most Positive Text": most_positive['text'],
    "Most Positive Score": most_positive['sentiment'],
    "Most Negative Text": most_negative['text'],
    "Most Negative Score": most_negative['sentiment'],
    "Overall Sentiment": overall_sentiment
}

results_df = pd.DataFrame([results])
results_df.to_csv('results/TextBlob/textblob_summary.csv', index=False)

print(f"Most Positive: {most_positive['text']} (TextBlob Score: {most_positive['sentiment']})")
print(f"Most Negative: {most_negative['text']} (TextBlob Score: {most_negative['sentiment']})")
vibe = 'good' if overall_sentiment > 0 else 'not good' if overall_sentiment < 0 else 'neutral'
print(f"The overall 'vibe' of the Georgia Tech subreddit is {vibe} with an average sentiment score of {overall_sentiment:.2f}.")
print("All plots and summary information (TextBlob) saved in 'results' folder.")
