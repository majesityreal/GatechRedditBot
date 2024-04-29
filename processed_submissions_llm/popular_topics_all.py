import pandas as pd
import os

def read_and_process_files(directory):
    all_data = pd.DataFrame()
    
    # loop through all CSV files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('_generalized.csv'):
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path, usecols=['generalized_topic', 'score'])
            all_data = pd.concat([all_data, df], ignore_index=True)


    return all_data

def split_and_aggregate_topics(df):
    # split the 'generalized_topic' into individual topics and explode them into separate rows
    df['topic'] = df['generalized_topic'].str.split(', ')
    df_exploded = df.explode('topic')
    
    # aggregate scores for each topic
    topic_scores = df_exploded.groupby('topic')['score'].agg(['count', 'sum']).reset_index()
    topic_scores.columns = ['Topic', 'Frequency', 'Total Score']

    # sort topics by Total Score
    topic_scores = topic_scores.sort_values(by='Total Score', ascending=False)
    
    return topic_scores


current_directory = os.getcwd()
df = read_and_process_files(current_directory)
popular_topics = split_and_aggregate_topics(df)

popular_topics.to_csv('popular_topics_overall.csv', index=False)
print(popular_topics.head())  # print top topics to the console for quick review

