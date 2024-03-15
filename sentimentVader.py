import os
import json
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from datetime import datetime

# Initialize VADER
analyzer = SentimentIntensityAnalyzer()

# load  data
with open('gatech_posts_with_comments.json') as file:
    data = json.load(file)

# func to calculate VADER sentiment
def vader_sentiment(text):
    return analyzer.polarity_scores(text)['compound']

# extract data from json
posts = []
for item in data:
    created_utc = datetime.utcfromtimestamp(item['created_utc']).strftime('%Y-%m-%d')
    post_score = item['score']
    post_sentiment = vader_sentiment(item['title'] + '. ' + item['selftext'])
    posts.append({'type': 'post', 'text': item['title'], 'vader_sentiment': post_sentiment, 'score': post_score, 'date': created_utc})

    for comment in item['comments']:
        comment_score = comment['score']
        comment_sentiment = vader_sentiment(comment['body'])
        posts.append({'type': 'comment', 'text': comment['body'], 'vader_sentiment': comment_sentiment, 'score': comment_score, 'date': created_utc})


df = pd.DataFrame(posts)

# adjusted sentiment score
df['adjusted_vader_sentiment'] = df['vader_sentiment']*df['score']

# Overall Sentiment
overall_sentiment = df['vader_sentiment'].mean()

# Sentiment Distribution plot
plt.figure()
df['vader_sentiment'].hist(bins=20)
plt.title('VADER Sentiment Distribution')
plt.xlabel('Sentiment Score')
plt.ylabel('Frequency')
plt.savefig('results/Vader/sentiment_distribution.png')

# post vs comment Sentiment plot
plt.figure()
df.groupby('type')['vader_sentiment'].mean().plot(kind='bar')
plt.title('Average VADER Sentiment: Post vs Comment')
plt.ylabel('Average Sentiment Score')
plt.savefig('results/Vader/post_vs_comment_sentiment.png')

# Temporal Trends
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)
plt.figure()
df.resample('M')['vader_sentiment'].mean().plot()
plt.title('Monthly Sentiment Trends')
plt.ylabel('Average Sentiment')
plt.savefig('results/Vader/monthly_sentiment_trends.png')


# sentiment Consistency
post_comment_sentiment = df.pivot_table(index='date', columns='type', values='vader_sentiment', aggfunc='mean')
plt.figure()
post_comment_sentiment.plot()
plt.title('Post vs Comment Sentiment Over Time')
plt.ylabel('Sentiment')
plt.savefig('results/Vader/post_comment_sentiment_over_time.png')


# find most positive and negative texts
most_positive = df[df['vader_sentiment'] == df['vader_sentiment'].max()].iloc[0]
most_negative = df[df['vader_sentiment'] == df['vader_sentiment'].min()].iloc[0]


results = {
    "Most Positive Text": most_positive['text'],
    "Most Positive Score": most_positive['vader_sentiment'],
    "Most Negative Text": most_negative['text'],
    "Most Negative Score": most_negative['vader_sentiment'],
    "Overall Sentiment": overall_sentiment
}



results_df = pd.DataFrame([results])
results_df.to_csv('results/Vader/summary.csv', index=False)

print(f"Most Positive: {most_positive['text']} (VADER Score: {most_positive['vader_sentiment']})")
print(f"Most Negative: {most_negative['text']} (VADER Score: {most_negative['vader_sentiment']})")

vibe = 'good' if overall_sentiment > 0 else 'not good' if overall_sentiment < 0 else 'neutral'
print(f"The overall 'vibe' of the Georgia Tech subreddit is {vibe} with an average sentiment score of {overall_sentiment:.2f}.")
print("All plots and summary information (Vader) saved in 'results' folder.")
