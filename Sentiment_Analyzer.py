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
from transformers import BertTokenizer, BertForSequenceClassification, AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
import torch

def Sentiment_Analysis1(df):
    model = BertForSequenceClassification.from_pretrained("ProsusAI/finbert",num_labels=3)
    tokenizer = BertTokenizer.from_pretrained("ProsusAI/finbert")
    
    nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

    def sentiment_label(title, nlp):
        results = nlp(title)
        label = results[0]['label']
        return label
    # FIX THIS WHEN YOU HAVE TIME
    def sentiment_score(title, nlp):
        results = nlp(title)
        score = results[0]['score']
        return score

    df['date'] = pd.to_datetime(df['date']).dt.date
    
    df['Sentiment Label'] = df['title'].apply(lambda title: sentiment_label(title, nlp))
    df['Sentiment Score'] = df['title'].apply(lambda title: sentiment_score(title, nlp))
    # print(df['Sentiment Label'].value_counts())
    # print(df.tail(20))
    net_sent_score = 0
    for row in range(df.shape[0]):
        if df.iloc[row]['Sentiment Label'] == 'negative': # negative
            net_sent_score -= df.iloc[row]['Sentiment Score']
        elif df.iloc[row]['Sentiment Label'] == 'positive': # positive
            net_sent_score += df.iloc[row]['Sentiment Score']
        else: # neutral
            pass

    net_sent_score = net_sent_score / df.shape[0]
    # net_sent_score += Sentiment_Analysis2(df)
    return net_sent_score

def Sentiment_Analysis2(df):
    tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
    model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
    
    def sentiment_score(title, tokenizer, model):
        tokens = tokenizer.encode(title, return_tensors= 'pt')
        results = model(tokens)
        scores = int(torch.argmax(results.logits))+1
        scores_stand = (scores - 3.5452)/2
        if scores_stand < -1:
            scores_stand = -1
        return scores_stand
    
    df['date'] = pd.to_datetime(df['date']).dt.date

    df['Sentiment Score'] = df['title'].apply(lambda title: sentiment_score(title, tokenizer, model))
    mean_sentiment = df.groupby(['date']).mean(['Sentiment Score'])

    print(mean_sentiment.tail())
    overall_sentiment_series = mean_sentiment.mean()
    overall_sentiment = overall_sentiment_series.iloc[0]
    print(overall_sentiment)
    return overall_sentiment