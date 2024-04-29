import pandas as pd
import os
import re

def process_csv_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('filtered.csv'):
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path)

            # df['topic'] = df['topic'].apply(transform_topics)
            df['topic'] = df['topic'].str.lower()
            check_format(df, file_path)
            check_for_errors(df, file_path)

            df.to_csv(file_path, index=False)
            print(f"Updated file saved: {file_path}")

def transform_topics(topics):
    # check if the topics are in the numbered list format
    if re.match(r'^\d+\.\s*[\w\s/,-]+(?:\n\d+\.\s*[\w\s/,-]+)*$', topics, flags=re.DOTALL):
        print("fixing")
        new_topics = re.sub(r'\d+\.\s+', '', topics)  # remove the numbers
        new_topics = new_topics.replace('\n', ', ')  # replace newlines with commas
        new_topics = new_topics.lower()
        return new_topics.strip()
    return topics

def check_format(df, file_path): # we check formatting
    incorrect_format = df['generalized_topic'].apply(lambda x: bool(re.search(r'\d+\.\s*[\w\s/,\-\(\)]+', x)))
    if incorrect_format.any():
        print(f"Entries in incorrect format found in {file_path}:")
        print(df.loc[incorrect_format, 'generalized_topic'])

def check_for_errors(df, file_path):# we check formatting
    error_entries = df['generalized_topic'] == "error"
    if error_entries.any():
        print(f"'Error' entries found in {file_path}:")
        print(df.loc[error_entries, 'generalized_topic'])

process_csv_files(os.getcwd())
