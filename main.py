"""
TODO:
Build Sentiment Analysis
Run tokens from input to Sentiment Analysis
Return Graph Showing how the sentiment of the stock has been doing, mostly for verification of validity of Model
Return Sentiment and Cool Message for Buy or No Buy
Can Also have cool title Screen Showing the things built using Tkinter if we have time
"""
from Sentiment_Analysis_New import Sentiment_Analysis
from web_scraper import web_scraper

def main():
    Sentiment_Analysis(web_scraper())

main()