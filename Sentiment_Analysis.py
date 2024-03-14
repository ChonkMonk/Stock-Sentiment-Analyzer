import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline

def Sentiment_Analysis(df, ticker):
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

    df['date'] = pd.to_datetime(df['date']).dt.date
    
    df['Sentiment Label'] = df['title'].apply(lambda title: sentiment_label(title, nlp))
    df['Sentiment Score'] = df['title'].apply(lambda title: sentiment_score(title, nlp))

    mean_sentiment = df.groupby(['Sentiment Label'])['Sentiment Score'].mean().reset_index()
    max_score_idx = mean_sentiment['Sentiment Score'].idxmax()
    mean_sent_lab = mean_sentiment.loc[max_score_idx, 'Sentiment Label']

    print(f'AMD Sentiment Label:')
    print(mean_sent_lab)
    print(f'With a Score of:')
    print(mean_sentiment.iloc[max_score_idx]['Sentiment Score'])