"""
TODO:
Return Graph Showing how the sentiment of the stock has been doing, mostly for verification of validity of Model
Use ML to adjust weights such that it fits stock price data?

Weight based on mean for every article rather than by day
Weightings still really bad
"""
from backend.Sentiment_Analyzer import Sentiment_Analyzer
from transformers import BertTokenizer, BertForSequenceClassification, AutoTokenizer, AutoModelForSequenceClassification
from backend.web_scraper import web_scraper

model1 = BertForSequenceClassification.from_pretrained("ProsusAI/finbert",num_labels=3)
tokenizer1 = BertTokenizer.from_pretrained("ProsusAI/finbert")
model2 = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
tokenizer2 = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

Analyzer1 = Sentiment_Analyzer(weighting = 1, model = model1, tokenizer = tokenizer1)
Analyzer2 = Sentiment_Analyzer(weighting = 1, model = model2, tokenizer = tokenizer2)

def main():
    df, ticker = web_scraper()
    Net_sentiment = Analyzer1.analyze(df, ticker) + Analyzer2.analyze(df, ticker)
    print(Net_sentiment)
main()