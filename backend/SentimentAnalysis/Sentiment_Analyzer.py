"""
How Mean Sentiment should be taken:
if label is negative:
    total score -= negative score
if label is neutral:
    total score no change
if label is positive:
    total score += positive score


New 3 AM revelations:
    Turn the final thing into a standard normal distribution for each sentiment analyzer
        Trial and error to see which one has the best shape (not standardized)
            ie trying the weights by day, trying the weights by article etc.
Can turn the dataframes into numpy arrays instead to speed up computing
    ie one 
"""
import pandas as pd
from transformers import pipeline
from web_scraper import web_scraper

class Sentiment_Analyzer:
    def __init__(self, weighting, model, tokenizer, stdev, mean):
        self.weight = weighting
        self.model = model
        self.tokenizer = tokenizer
        self.nlp = pipeline("sentiment-analysis",model = self.model, tokenizer = self.tokenizer)
        self.stdev = stdev
        self.mean = mean

    def sentiment_label(self, title, nlp):
        results = nlp(title)
        label = results[0]['label']
        return label
    def sentiment_score(self, title, nlp):
        results = nlp(title)
        score= results[0]['score']
        return score
    def analyzer_finbert(self, df, ticker):
        df['Sentiment Label'] = df['title'].apply(lambda title: self.sentiment_label(title, self.nlp))
        df['Sentiment Score'] = df['title'].apply(lambda title: self.sentiment_score(title, self.nlp))
        net_sent_score = 0
        for row in range(df.shape[0]):
            if df.iloc[row]['Sentiment Label'] == 'negative':
                net_sent_score -= df.iloc[row]['Sentiment Score']
            elif df.iloc[row]['Sentiment Label'] == 'positive':
                net_sent_score += df.iloc[row]['Sentiment Score']
            else:
                pass
        net_sent_score = net_sent_score / df.shape[0]
        net_sent_score = (net_sent_score - self.mean)/self.stdev
        return self.weight*net_sent_score
    
    def analyzer_bert(self, df, ticker):
        df['Sentiment Label'] = df['title'].apply(lambda title: self.sentiment_label(title, self.nlp))
        df['Sentiment Score'] = df['title'].apply(lambda title: self.sentiment_score(title, self.nlp))
        net_sent_score = 0
        weightings_mid = 0.5
        for row in range(df.shape[0]):
            if df.iloc[row]['Sentiment Label'] == '5 stars':
                net_sent_score += df.iloc[row]['Sentiment Score']
            elif df.iloc[row]['Sentiment Label'] == '4 stars':
                net_sent_score += weightings_mid * df.iloc[row]['Sentiment Score']
            elif df.iloc[row]['Sentiment Label'] == '3 stars':
                pass
            elif df.iloc[row]['Sentiment Label'] == '2 stars':
                net_sent_score -= weightings_mid*df.iloc[row]['Sentiment Score']
            elif df.iloc[row]['Sentiment Label'] == '1 star':
                net_sent_score -= df.iloc[row]['Sentiment Score']
        net_sent_score = net_sent_score / df.shape[0]
        # net_sent_score = (net_sent_score - self.mean)/self.stdev
        return self.weight*net_sent_score
    
    def set_std_mean(self, df):
        self.stdev = df['Sentiment Score'].std()
        self.mean = df['Sentiment Score'].mean()
        return (self.stdev, self.mean)