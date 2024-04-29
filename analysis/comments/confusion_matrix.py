import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix

# we define function to convert sentiment values to categories
def convert_sentiment(sentiment, method):
    if method == "ChatGPT":
        if "Positive" in sentiment:
            return "Positive"
        elif "Negative" in sentiment:
            return "Negative"
        elif "Neutral" in sentiment:
            return "Neutral"
        else:
            return "Unknown"
    elif method == "VADER":
        if "positive" in sentiment:
            return "Positive"
        elif "negative" in sentiment:
            return "Negative"
        elif "neutral" in sentiment:
            return "Neutral"
        else:
            return "Unknown"
    elif method == "TextBlob":
        if "positive" in sentiment:
            return "Positive"
        elif "negative" in sentiment:
            return "Negative"
        elif "neutral" in sentiment:
            return "Neutral"
        else:
            return "Unknown"
    else:
        return "Unknown"


# function to generate confusion matrix
def generate_confusion_matrix(file1, file2):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    # extract sentiments and convert to categories
    chatGPT = df1['sentiment'].apply(convert_sentiment, method="ChatGPT")
    VADER = df2['VADER sentiment'].apply(convert_sentiment, method="VADER")
    TextBlob = df2['TextBlob sentiment'].apply(convert_sentiment, method="TextBlob")

    # gen confusion matrices
    cm_chatgpt_vader = confusion_matrix(chatGPT, VADER, labels=["Positive", "Negative", "Neutral"])
    cm_chatgpt_textblob = confusion_matrix(chatGPT, TextBlob, labels=["Positive", "Negative", "Neutral"])
    cm_vader_textblob = confusion_matrix(VADER, TextBlob, labels=["Positive", "Negative", "Neutral"])
    
    return cm_chatgpt_vader, cm_chatgpt_textblob, cm_vader_textblob


total_cm_chatgpt_vader_percent = np.zeros((3, 3))
total_cm_chatgpt_textblob_percent = np.zeros((3, 3))
total_cm_vader_textblob_percent = np.zeros((3, 3))
total_comments = 0

folder_path = os.getcwd()  # get current working directory
for filename in os.listdir(folder_path):
    if filename.endswith("filtered.csv"):
        file1 = os.path.join(folder_path, filename)
        file2 = os.path.join(folder_path, filename.replace("filtered.csv", "filtered_results.csv"))
        
        if os.path.isfile(file2):  # check if the corresponding "_results" file exists
            # gen confusion matrices
            df4 = pd.read_csv(file1)  # load df1
            cm_chatgpt_vader, cm_chatgpt_textblob, cm_vader_textblob = generate_confusion_matrix(file1, file2)
            
            # add to total confusion matrices
            total_cm_chatgpt_vader_percent += cm_chatgpt_vader
            total_cm_chatgpt_textblob_percent += cm_chatgpt_textblob
            total_cm_vader_textblob_percent += cm_vader_textblob
            
            # count total number of comments
            total_comments += len(df4)

# normalize
total_cm_chatgpt_vader_percent /= total_comments
total_cm_chatgpt_textblob_percent /= total_comments
total_cm_vader_textblob_percent /= total_comments

labels = ["Positive", "Negative", "Neutral"]

# plotting ChatGPT vs VADER confusion matrix
plt.figure(figsize=(8, 6))
plt.imshow(total_cm_chatgpt_vader_percent, interpolation='nearest', cmap=plt.cm.Blues)
for i in range(len(labels)):
    for j in range(len(labels)):
        plt.text(j, i, "{:.2f}%".format(total_cm_chatgpt_vader_percent[i][j] * 100), horizontalalignment="center", color="black")
plt.title("Confusion Matrix (ChatGPT vs VADER) - Comments")
tick_marks = np.arange(len(labels))
plt.xticks(tick_marks, labels)
plt.yticks(tick_marks, labels)
plt.xlabel('VADER')
plt.ylabel('ChatGPT')
plt.tight_layout()
plt.savefig("confusion_matrix_chatgpt_vs_vader_comments_percent.png")
plt.show()

# plot ChatGPT vs TextBlob confusion matrix
plt.figure(figsize=(8, 6))
plt.imshow(total_cm_chatgpt_textblob_percent, interpolation='nearest', cmap=plt.cm.Blues)
for i in range(len(labels)):
    for j in range(len(labels)):
        plt.text(j, i, "{:.2f}%".format(total_cm_chatgpt_textblob_percent[i][j] * 100), horizontalalignment="center", color="black")
plt.title("Confusion Matrix (ChatGPT vs TextBlob) - Comments")
tick_marks = np.arange(len(labels))
plt.xticks(tick_marks, labels)
plt.yticks(tick_marks, labels)
plt.xlabel('TextBlob')
plt.ylabel('ChatGPT')
plt.tight_layout()
plt.savefig("confusion_matrix_chatgpt_vs_textblob_comments_percent.png")
plt.show()

# plot VADER vs TextBlob confusion matrix
plt.figure(figsize=(8, 6))
plt.imshow(total_cm_vader_textblob_percent, interpolation='nearest', cmap=plt.cm.Blues)
for i in range(len(labels)):
    for j in range(len(labels)):
        plt.text(j, i, "{:.2f}%".format(total_cm_vader_textblob_percent[i][j] * 100), horizontalalignment="center", color="black")
plt.title("Confusion Matrix (VADER vs TextBlob) - Comments")
tick_marks = np.arange(len(labels))
plt.xticks(tick_marks, labels)
plt.yticks(tick_marks, labels)
plt.xlabel('TextBlob')
plt.ylabel('VADER')
plt.tight_layout()
plt.savefig("confusion_matrix_vader_vs_textblob_posts_percent.png")
plt.show()