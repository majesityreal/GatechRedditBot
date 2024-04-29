import extract_processed_submissions as eps
import extract_processed_comments as epc

import json
import sys
import glob
import os

import statistics

from datetime import datetime
import csv

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as stats

def calculate_metrics(df):
    # grouping by month, season, and semester and calculating mean, median, and variance
    metrics = pd.DataFrame({
        'mean': df.groupby('month')['VADER sentiment score'].mean(),
        'median': df.groupby('month')['VADER sentiment score'].median(),
        'variance': df.groupby('month')['VADER sentiment score'].var(),
    })


    season_metrics = pd.DataFrame({
        'mean': df.groupby('season')['VADER sentiment score'].mean(),
        'median': df.groupby('season')['VADER sentiment score'].median(),
        'variance': df.groupby('season')['VADER sentiment score'].var(),
    })

    semester_metrics = pd.DataFrame({
        'mean': df.groupby('semester')['VADER sentiment score'].mean(),
        'median': df.groupby('semester')['VADER sentiment score'].median(),
        'variance': df.groupby('semester')['VADER sentiment score'].var(),
    })


    return metrics, season_metrics, semester_metrics

# plot metrics
def plot_metrics(metrics, title):
    output_dir = 'SA_plots'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    fig, ax = plt.subplots()
    ax.plot(metrics.index, metrics['mean'], label='Mean', marker='o', linestyle='-')
    ax.plot(metrics.index, metrics['median'], label='Median', marker='x', linestyle='--')
    
    # we add error bars for variance
    ax.errorbar(metrics.index, metrics['mean'], yerr = metrics['variance']**0.5, fmt='o', label='Std Dev (Mean)' ,capsize=5,)
    
    ax.set_title(title)
    ax.set_ylabel('Sentiment Score')

    ax.set_xlabel('Time Period')

    ax.legend()
    
    plt.xticks(rotation=45)  # we rotate labels to avoid overlap
    plt.tight_layout()  # then adjust layout to make room for label rotation
    

    filename = f"{title.replace(' ', '_').replace('/', '_').replace(',', '')}.png"
    filepath = os.path.join(output_dir, filename)

    plt.savefig(filepath)
    plt.close(fig)


def plot_normal_distribution(df, column_name, title, type):

    mu = df[column_name].mean()
    sigma = df[column_name].std()
    
    num_bins = 50
    
    fig, ax = plt.subplots()
    n, bins, patches = ax.hist(df[column_name].dropna(), num_bins, density = True,  color='blue',  edgecolor='black', alpha=0.75,)

    # we add a 'best fit' line for the normal distribution
    y = stats.norm.pdf(bins, mu, sigma)
    ax.plot(bins, y, '--', color='red')

    ax.set_xlabel('Sentiment Score')
    ax.set_ylabel('Probability Density')
    ax.set_title(rf'Histogram of {type} Sentiment Scores: $\mu=' + f'{mu:.2f},\ \sigma={sigma:.2f}$, bins: {num_bins}')

    fig.tight_layout()

    output_dir = 'SA_plots'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = f"{title.replace(' ', '_').replace('/', '_').replace(',', '')}.png"
    filepath = os.path.join(output_dir, filename)

    plt.savefig(filepath)
    plt.close(fig)

# posts vs comments sentiment
def plot_Submissions_vs_Comments_Sentiment(df_submissions, df_comments, title):
    submissions_sentiment = df_submissions['VADER sentiment score'].mean()
    comments_sentiment = df_comments['VADER sentiment score'].mean()
    
    average_scores = {
        'Posts': submissions_sentiment,
        'Comments': comments_sentiment,
    }

    df_plot = pd.DataFrame(list(average_scores.items()), columns=['Type', 'Average VADER Sentiment Score'])
    
    fig, ax = plt.subplots()
    df_plot.set_index('Type')['Average VADER Sentiment Score'].plot(kind = 'bar', color=['blue', 'green'], ax=ax)

    ax.set_title('Average Sentiment Score: Posts vs Comments')
    ax.set_ylabel('Average VADER Sentiment Score')
    ax.set_xlabel('Type')
    fig.tight_layout()

    output_dir = 'SA_plots'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = f"{title.replace(' ', '_').replace('/', '_').replace(',', '')}.png"
    filepath = os.path.join(output_dir, filename)
    
    plt.savefig(filepath)
    plt.close(fig)


# run our instances to compare
# eps instance
df_submissions = eps.run()

submissions_monthly_metrics, submissions_season_metrics, submissions_semester_metrics = calculate_metrics(df_submissions)

print(submissions_monthly_metrics['mean'])
print(submissions_season_metrics['mean'])
print(submissions_semester_metrics['mean'])

print("Overall Posts Sentiment Score: ", df_submissions['VADER sentiment score'].mean())

plot_metrics(submissions_monthly_metrics, 'Posts Monthly Sentiment Trends')
plot_metrics(submissions_season_metrics, 'Posts Seasonal Sentiment Trends')
plot_metrics(submissions_semester_metrics, 'Posts Semester Sentiment Trends')

plot_normal_distribution(df_submissions, 'VADER sentiment score', 'Posts Overall Sentiment Distributions', 'Posts')

# spec instances
df_comments = epc.run()

comments_monthly_metrics, comments_season_metrics, comments_semester_metrics = calculate_metrics(df_comments)

print(comments_monthly_metrics['mean'])
print(comments_season_metrics['mean'])
print(comments_semester_metrics['mean'])

print("Overall Comments Sentiment Score: ", df_comments['VADER sentiment score'].mean())

plot_metrics(comments_monthly_metrics, 'Comments Monthly Sentiment Trends')
plot_metrics(comments_season_metrics, 'Comments Seasonal Sentiment Trends')
plot_metrics(comments_semester_metrics, 'Comments Semester Sentiment Trends')

plot_normal_distribution(df_comments, 'VADER sentiment score', 'Comments Overall Sentiment Distributions', 'Comments')



# across posts and comments
plot_Submissions_vs_Comments_Sentiment(df_submissions, df_comments, "Posts vs. Comments Overall Sentiment")