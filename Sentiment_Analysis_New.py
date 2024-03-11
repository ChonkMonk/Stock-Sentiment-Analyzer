import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from datetime import date
import matplotlib.pyplot as plt

def Sentiment_Analysis(df):
    tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
    model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
    df['date'] = pd.to_datetime(df['date']).dt.date
    
    df['Sentiment Scores'] = df['title'].apply(lambda title: sentiment_score(title, tokenizer, model))
    mean_sentiment = df['Sentiment Scores'].mean()
    mean_sentiment_date = df.groupby(['date']).mean(['Sentiment Scores'])

    print(mean_sentiment_date.tail(10))
    # overall_sentiment_series = mean_sentiment.mean()
    # overall_sentiment = overall_sentiment_series.iloc[0]
    overall_sentiment = mean_sentiment

    if overall_sentiment >= 3:
        print(f'Overall Sentiment has a rating of: {overall_sentiment}')
        print('Might be a good Idea to buy!')
    else:
        print(f'Overall Sentiment has a rating of: {overall_sentiment}')
        print('Should probably not buy')

def sentiment_score(title, tokenizer, model):
    tokens = tokenizer.encode(title, return_tensors= 'pt')
    results = model(tokens)
    scores = int(torch.argmax(results.logits))+1
    return scores