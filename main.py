"""
TODO:
Build Sentiment Analysis
Run tokens from input to Sentiment Analysis
Return Graph Showing how the sentiment of the stock has been doing, mostly for verification of validity of Model
Return Sentiment and Cool Message for Buy or No Buy
Can Also have cool title Screen Showing the things built using Tkinter if we have time

Weight based on mean for every article rather than by day
"""
from Sentiment_Analyzer import Sentiment_Analysis1, Sentiment_Analysis2
from web_scraper import web_scraper

def main():
    df, ticker = web_scraper()
    weight1 = 1
    weight2 = 2

    net_sent_score = weight1*Sentiment_Analysis1(df)
    net_sent_score += weight2*Sentiment_Analysis2(df)

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
    
main()