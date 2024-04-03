import yfinance as yf

class ticker:
    def __init__(self, ticker:str, quantity):
        self.ticker = yf.Ticker(ticker.upper())
        self.quantity = quantity

    def __repr__(self):
        return str(self.ticker)

    def get_data(self, timeperiod):
        try:
            data = self.ticker.history(timeperiod)
            return data['Close']
        except:
            raise Exception('Bro Enter a Time Period: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo')
        
    def get_current_price(self):
        history = self.ticker.history()
        last_price = history['Close'].iloc(-1) # only returns last closing price
        return last_price