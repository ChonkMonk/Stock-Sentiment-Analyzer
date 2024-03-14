from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
import pandas as pd
import torch

df = pd.DataFrame({'ticker':['AMD','AMD','AMD','AMD'],
                  'date':['10-3-2024','15-3-2024','14-3-2024','13-3-2024'],
                  'title':["Why AMD doesn't have to be a winner in AI chips", "It's another tough day for chip stocks", "Nvidia to showcase new blackwell GPU at GTC event", "10 Best Semiconductor ETFs"]})

model = BertForSequenceClassification.from_pretrained("ahmedrachid/FinancialBERT-Sentiment-Analysis",num_labels=3)
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

df['Sentiment Label'] = df['title'].apply(lambda title: sentiment_label(title, nlp))
df['Sentiment Score'] = df['title'].apply(lambda title: sentiment_score(title, nlp))
print(df.head())
mean_sentiment = df.groupby(['Sentiment Label'])['Sentiment Score'].mean()
mean_sent_int = max()
mean_sentiment_date = df.groupby(['date']).mean(['Sentiment Scores'])

print(mean_sentiment_date)
print(mean_sentiment)

moon = sentiment_score('NVDIA STOCKS TO THE MOON', nlp)

print(moon)
