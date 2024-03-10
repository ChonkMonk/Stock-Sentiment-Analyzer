import re
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

def web_scraper():
    finviz_url = "https://finviz.com/quote.ashx?t="
    ticker = input('What Ticker Would you Like to Check the Sentiment of?\n')

    news_tables = {}

    url = finviz_url + ticker

    req = Request(url = url, headers = {'user-agent': 'mega-chonk'})
    response = urlopen(req)

    html = BeautifulSoup(response, 'html')
    news_table = html.find(id = 'news-table')
    news_tables[ticker] = news_table
        
    parsed_data = []

    for ticker, news_table in news_tables.items():
        for row in news_table.findAll('tr'):
            title = row.a.text
            date_data = row.td.text
            date_data = re.sub(r"\r\n", "", date_data)
            date_data = re.sub(r"\s+", " ", date_data)
            date_data = re.sub(r"^\s|\s$", "", date_data)
            date_data = date_data.split(" ")

            if date_data[0].lower() == 'today':
                date_data[0]= date.today()
                time = date_data[1]
            if len(date_data) == 1:
                time = date_data[0]
            else:
                date_article = date_data[0]
                time = date_data[1]

            parsed_data.append([ticker, date_article, time, title])

    # print(parsed_data)

    df = pd.DataFrame(parsed_data, columns = ['ticker', 'date', 'time', 'title'])
    return df

# vader = SentimentIntensityAnalyzer()

# f = lambda title: vader.polarity_scores(title)['compound']
# df['compound'] = df['title'].apply(f)
# df['date'] = pd.to_datetime(df['date']).dt.date

# print(df.head)

# today = date.today()
# month, year = (today.month - 1, today.year) if today.month != 12 else (12, today.year - 1) 
# start_date = today.replace(day = today.day, month = month, year = year)

# mean_df = df.groupby(['ticker', 'date']).mean(['compound'])
# mean_df = mean_df.unstack()
# mean_df = mean_df.xs('compound', axis = 'columns').transpose()
# mean_df = mean_df[mean_df.index > start_date]

# print(mean_df.head)

# plt.figure(figsize = (10,8))
# mean_df.plot(kind = 'bar')
# plt.show()

# print(mean_df)