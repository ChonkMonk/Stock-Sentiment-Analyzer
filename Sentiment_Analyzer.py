"""
How Mean Sentiment should be taken:
if label is negative:
    total score -= negative score
if label is neutral:
    total score no change
if label is positive:
    total score += positive score
"""
import pandas as pd
from transformers import pipeline
from web_scraper import web_scraper

class Sentiment_Analyzer:
    def __init__(self, weighting, model, tokenizer):
        self.weight = weighting
        self.model = model
        self.tokenizer = tokenizer
        self.nlp = pipeline("sentiment-analysis", model=self.model, tokenizer=self.tokenizer)

    # theres probably a way to make this code cleaner but idk how to do it ehe~
    def sentiment_label(self, title, nlp):
        results = nlp(title)
        label = results[0]['label']
        return label
    def sentiment_score(self, title, nlp):
        results = nlp(title)
        score = results[0]['score']
        return score

    def analyze(self, df, ticker):
        df['Sentiment Label'] = df['title'].apply(lambda title: self.sentiment_label(title, self.nlp))
        df['Sentiment Score'] = df['title'].apply(lambda title: self.sentiment_score(title, self.nlp))
        net_sent_score = 0
        for row in range(df.shape[0]):
            if df.iloc[row]['Sentiment Label'] == 'negative': # negative
                net_sent_score -= df.iloc[row]['Sentiment Score']
            elif df.iloc[row]['Sentiment Label'] == 'positive': # positive
                net_sent_score += df.iloc[row]['Sentiment Score']
            else: # neutral
                pass

        net_sent_score = net_sent_score / df.shape[0]
        return self.weight*net_sent_score