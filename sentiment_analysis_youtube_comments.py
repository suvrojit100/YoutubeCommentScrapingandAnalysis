## Imports

import pandas as pd
import csv
import nltk
import os.path as checkcsv

## Downloads

# Download the VADER lexicon if not already downloaded
nltk.download('vader_lexicon')

def sepposnegcom(comment_file):

    ## Reading Dataset

    dataset = pd.read_csv(comment_file, encoding_errors='ignore')
    dataset = dataset.iloc[:, 0:]

    ## Sentiment analysis of comments using VADER sentiment analyzer

    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    analyser = SentimentIntensityAnalyzer()

    def vader_sentiment_result(sent):
        scores = analyser.polarity_scores(sent)

        if scores["neg"] > scores["pos"]:
            return 0
        return 1

    dataset['vader_sentiment'] = dataset['Comment'].apply(lambda x : vader_sentiment_result(x))

    ## Separating Positive and Negative Comments

    for (sentiment), group in dataset.groupby(['vader_sentiment']):
        group.to_csv(f'{sentiment}.csv', index=False)
    
    if not checkcsv.exists('1.csv'):  # If 1.csv file does not exist, it creates one empty 1.csv file.
        with open('1.csv', 'w', encoding='UTF8', newline='') as f1:
            writer1 = csv.writer(f1)
            header1 = ['Empty', 'Empty', 'Empty']
            row1 = ['No Positive Comments', 'No Positive Comments', 'No Positive Comments']
            writer1.writerow(header1)
            writer1.writerow(row1)

    if not checkcsv.exists('0.csv'):  # If 0.csv file does not exist, it creates one empty 0.csv file.
        with open('0.csv', 'w', encoding='UTF8', newline='') as f0:
            writer0 = csv.writer(f0)
            header0 = ['Empty', 'Empty', 'Empty']
            row0 = ['No Negative Comments', 'No Negative Comments', 'No Negative Comments']
            writer0.writerow(header0)
            writer0.writerow(row0)
    
    pos = pd.read_csv("1.csv", engine='python').iloc[:, :-1]
    neg = pd.read_csv("0.csv", engine='python').iloc[:, :-1]

    pos.to_csv("Positive Comments.csv", index=False)
    neg.to_csv("Negative Comments.csv", index=False)

    video_positive_comments = str(len(pos)) + ' Comments'  # Finding total rows in positive comments
    video_negative_comments = str(len(neg)) + ' Comments'  # Finding total rows in negative comments
    
    if (pd.read_csv('1.csv', nrows=0).columns.tolist())[0] == 'Empty':
        video_positive_comments = '0 Comments'
    if (pd.read_csv('0.csv', nrows=0).columns.tolist())[0] == 'Empty':
        video_negative_comments = '0 Comments'

    ## return function
    return "Positive Comments.csv", "Negative Comments.csv", video_positive_comments, video_negative_comments
