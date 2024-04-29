import pandas as pd
import os

def process_file(file_path):
    df = pd.read_csv(file_path, usecols=['topic', 'score', 'sentiment'])

    # split the 'generalized_topic' into individual topics and explode them into separate rows
    df['topic'] = df['topic'].str.split(', ')
    df_exploded = df.explode('topic')

    # aggregate scores and sentiments for each topic
    aggregation_functions = {
        'score': ['count', 'sum'],
        'sentiment': lambda x: {
            'Positive': (x == 'Positive').sum(),
            'Negative': (x == 'Negative').sum(),
            'Neutral': (x == 'Neutral').sum()
        }
    }
    topic_scores = df_exploded.groupby('topic').agg(aggregation_functions).reset_index()
    topic_scores.columns = ['Topic', 'Frequency', 'Total Score', 'Sentiment']
    # split the sentiment dictionary into separate columns
    topic_scores[['Positive', 'Negative', 'Neutral']] = topic_scores['Sentiment'].apply(pd.Series)
    topic_scores.drop(columns=['Sentiment'], inplace=True)

    # sort topics by Total Score
    topic_scores = topic_scores.sort_values(by='Total Score', ascending=False)

    return topic_scores

def process_files_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith('_filtered.csv'):
            file_path = os.path.join(directory, filename)
            popular_topics = process_file(file_path)
            
            # save the results to a CSV file
            output_path = os.path.splitext(file_path)[0] + '_popular_topics.csv'
            popular_topics.to_csv(output_path, index=False)
            print(f"Popular topics for {filename} saved to '{output_path}'.")

process_files_in_directory(os.getcwd())
