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
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline

def Sentiment_Analysis(df, ticker):
    model = BertForSequenceClassification.from_pretrained("ahmedrachid/FinancialBERT-Sentiment-Analysis",num_labels=2)
    tokenizer = BertTokenizer.from_pretrained("ahmedrachid/FinancialBERT-Sentiment-Analysis")
    
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
    print(df['Sentiment Label'].value_counts())
    print(df.tail(20))
    net_sent_score = 0
    for row in range(df.shape[0]):
        if df.iloc[row]['Sentiment Label'] == 'negative': # negative
            net_sent_score -= df.iloc[row]['Sentiment Score']
        elif df.iloc[row]['Sentiment Label'] == 'positive': # positive
            net_sent_score += df.iloc[row]['Sentiment Score']
        else: # neutral
            pass

    net_sent_score = net_sent_score / df.shape[0]

    if net_sent_score < 0:
        label = 'Negative'
    elif net_sent_score == 0:
        label = 'Neutral'
    elif net_sent_score > 0:
        label = 'Positive'
        
    print(f'{ticker} Sentiment Label:')
    print(label)
    print(f'With a Score of:')
    print(net_sent_score)