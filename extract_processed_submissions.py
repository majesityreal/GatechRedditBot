import json
import sys
import glob
import os

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

import statistics

from datetime import datetime
import csv

from textblob import TextBlob

import preprocess_data as pre
nltk.download('stopwords')

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# ensure the VADER lexicon is downloaded
nltk.download('vader_lexicon')

# the function is basically reading and processing json
def read_and_process_json(file_name):
    posts = []
    with open(file_name, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                post = json.loads(line)
                posts.append(post)
            except json.JSONDecodeError:
                continue
    return posts

def get_season(date):# grouoped by season 
    month = date.month
    if month in (3, 4, 5):
        return 'Spring'
    elif month in (6, 7, 8):
        return 'Summer'
    elif month in (9, 10, 11):
        return 'Fall'
    else:
        return 'Winter'

def get_academic_semester(date): # grouoped by academic semester
    month = date.month
    if month in (2, 3, 4, 5):
        return 'Spring_Semester'
    elif month in (6, 7, 8):
        return 'Summer_Break'
    elif month in (9, 10, 11, 12):
        return 'Fall_Semester'
    else:
        return 'Winter_Break'


def analyze_sentiments(posts):
     # initialize vader
    sia = SentimentIntensityAnalyzer()


    results = []
    results_for_metrices = []
    for post in posts:
        # get text to analyze
        text_to_analyze = post['title'] + '. ' + post.get('selftext', '') 

        # vader
        sia_text_to_analyze = pre.preprocess_text_VADER(text_to_analyze) # preprocessing text
        sia_sentiment = sia.polarity_scores(sia_text_to_analyze)

        # textblob
        tb_sia_text_to_analyze = pre.preprocess_text_TextBlob(text_to_analyze)# preprocessing text
        tb_sentiment = TextBlob(tb_sia_text_to_analyze).sentiment  # get TextBlob sentiment
        
        post_type = 'posts'  # assuming all entries are posts

        created_date = datetime.fromtimestamp(post['created_utc']).strftime('%m/%d/%Y')
        month = datetime.fromtimestamp(post['created_utc']).strftime('%m') # get month
        season = get_season(datetime.fromtimestamp(post['created_utc']))
        semester = get_academic_semester(datetime.fromtimestamp(post['created_utc']))

        # classifying our sentiments 
        sia_sentiment_type = 'positive' if sia_sentiment['compound'] >= 0.05 else 'neutral' if sia_sentiment['compound'] > -0.05 else 'negative'
    
        tb_sentiment_type = 'positive' if tb_sentiment.polarity >= 0.05 else 'negative' if tb_sentiment.polarity <= -0.05 else 'neutral'
        tb_polarity = tb_sentiment.polarity

        # tb_subjectivity = tb_sentiment.subjectivity

        results.append([post_type, tb_sia_text_to_analyze, sia_sentiment_type, sia_sentiment['compound'], tb_sentiment_type, tb_polarity, created_date])

        results_for_metrices.append([post_type, tb_sia_text_to_analyze, sia_sentiment_type, sia_sentiment['compound'],
                        tb_sentiment_type, tb_polarity, created_date, month, season, semester])

    return results, results_for_metrices

# write our results to csv
def write_results_to_csv(posts_data_list, original_filename, directory):
    csv_filename = original_filename.replace('_filtered.txt', '_filtered_results.csv') # create results file names
    csv_path = os.path.join(directory, csv_filename)
    with open(csv_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['type', 'text', 'VADER sentiment', 'VADER sentiment score', 'TextBlob sentiment', 'TextBlob sentiment score', 'date'])
        for post in posts_data_list:
            if isinstance(post, list) and len(post) == 7:
                writer.writerow(post)  # write a single row
            else:
                continue

# process all data
def process_directory(directory):
    pattern = os.path.join(directory, 'RS_20??-??_filtered.txt')
    file_list = glob.glob(pattern)
    results_for_metrices_list = []
    for file_name in file_list:
        if os.path.exists(file_name):
            posts = read_and_process_json(file_name)# read in comments
            sentiment_results, results_for_metrices = analyze_sentiments(posts) # analyze sentiments
            results_for_metrices_list.extend(results_for_metrices)
            result_directory = 'processed_submissions_SA_result/'
            write_results_to_csv(sentiment_results, os.path.basename(file_name), result_directory) # Write results
        else:
            print(f"Skipping: {file_name} (not found)")
    return results_for_metrices_list



def run():
    directory = 'processed_submissions/'
    results_for_metrices_list = process_directory(directory)

    df = pd.DataFrame(results_for_metrices_list, columns=['type', 'text', 'VADER sentiment', 'VADER sentiment score', 'TextBlob sentiment',
        'TextBlob sentiment score', 'date', 'month', 'season', 'semester'])

    return df
