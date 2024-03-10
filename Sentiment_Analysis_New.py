import numpy as np
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
# from bs4 import BeautifulSoup
# import re
# from urllib.request import urlopen, Request
from datetime import date
import matplotlib.pyplot as plt

def Sentiment_Analysis(df):
    tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
    model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

    df['date'] = pd.to_datetime(df['date']).dt.date
    lamb1 = lambda title: tokenizer.encode(title)
    lamb2 = lambda Score: int(torch.argmax(model(Score).logits)+1)

    df['Sentiment Scores'] = df['title'].apply(lamb1)
    df['Sentiment'] = df['Sentiment Scores'].apply(lamb2)

    today = date.today()
    month, year = (today.month - 1, today.year) if today.month != 12 else (12, today.year - 1) 
    start_date = today.replace(day = today.day, month = month, year = year)

    mean_sentiment = df.groupby(['ticker', 'date']).mean(['Sentiment Scores'])

    print(mean_sentiment.head())