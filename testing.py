from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
import pandas as pd
import torch

"""
How Mean Sentiment should be taken:
if label is negative:
    total score -= negative score
if label is neutral:
    total score no change
if label is positive:
    total score += positive score
"""


df = pd.DataFrame({'ticker':['AMD','AMD','AMD','AMD'],
                  'date':['10-3-2024','15-3-2024','14-3-2024','13-3-2024'],
                  'title':["Why AMD doesn't have to be a winner in AI chips", "It's another tough day for chip stocks", "Does Tesla Still Belong in the Magnificent Seven?"
, "10 Best Semiconductor ETFs"]})

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

# actual sentiment score on scale of -1 to 1
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

print(net_sent_score)
print(label)

# print(df.head())
# mean_sentiment = df.groupby(['Sentiment Label'])['Sentiment Score'].mean().reset_index()


# print(mean_sentiment)
# print(f'AMD Sentiment Label:')
# print(mean_sent_lab)
# print(f'With a Score of:')
# print(mean_sentiment.iloc[max_score_idx]['Sentiment Score'])
