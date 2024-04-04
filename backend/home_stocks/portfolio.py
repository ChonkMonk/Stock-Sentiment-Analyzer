import yfinance as yf
from ticker import ticker

class Portfolio:
    def __init__(self, ticker_list = [], bought_prices = {}, current_prices = {}, total_bought_prices = {}, total_current_prices = {}, weightings = {}, portfolio_value = 0):
        self.ticker_list = ticker_list # list of objects which includes their quantities
        self.bought_prices= bought_prices
        self.current_prices = current_prices
        self.total_bought_prices = total_bought_prices
        self.total_current_prices = total_current_prices
        self.weightings = weightings
        self.portfolio_value = portfolio_value

    def __repr__(self):
        return self.current_prices

    def buy_ticker(self, tk:str, quantity:int):
        if quantity == 0 or not quantity:
            raise Exception('Enter a non Zero Quantity')
        try:
            tk = tk.upper()
            tk = ticker(tk, quantity)
            self.ticker_list.append(tk)
            ticker_history = self.ticker.history()
            self.bought_prices[tk] = ticker_history['Close'].iloc(-1)
            self.total_bought_prices[tk] = tk.quantity * tk.get_current_price()
            self.reweight()
        except:
            raise Exception('An Uncaught Error Has Occured and I will not Catch it ehe')

    def remove_ticker(self, ticker):
        try:
            ticker = ticker.upper()
            self.ticker_list.remove(ticker)
            self.bought_prices.pop(ticker)
            self.current_prices.pop(ticker)
        except KeyError:
            raise KeyError('Ticker Not in Portfolio')
    
    # reweight readjusts portfolio value, current total prices, and weightings
    # O(n) time, O(n) space
    def reweight(self):
        self.portfolio_value = 0.
        for tk in self.ticker_list:
            # updates all things in current prices to most recent price
            total_price = tk.quantity * tk.get_current_price()
            self.current_prices[tk] = total_price
            self.total_current_prices[tk] = total_price 
            self.portfolio_value += total_price
        for tk in self.ticker_list:
            # updates weight
            self.weightings[tk] = self.total_current_prices[tk] / self.portfolio_value