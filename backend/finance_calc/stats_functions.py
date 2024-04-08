import pandas as pd

class finance_calc:
    def __init__(self, portfolio:pd.core.frame.DataFrame, market:pd.core.frame.DataFrame):
        self.portfolio = portfolio # entire dataset for tickers, includes Open, High, Low, CLose, Volume, Dividends, Splits
        self.market = market

    def get_std(self):
        temp_data = self.data.cpoy()
        temp_data['Percent Change'] = temp_data['Close'].pct_change()
        std = temp_data.std()['Percent Change']
        return std

    def get_corr(self):
        temp_port = self.data.copy()
        temp_port['Percent Change PORT'] = temp_port['Close'].pct_change()
        temp_spy = self.market.copy()
        temp_spy['Percent Change SPY'] = temp_spy['Close'].pct_change()
        
        correl_df = temp_spy.merge(temp_port, left_index = True, right_index = True)
        correl_df_pct = correl_df[['Percent Change PORT','Percent Change SPY']]
        correl_matrix = correl_df_pct.corr()
        pct_correl_coeff = correl_matrix.loc['Percent Change Port','Percent Change SPY']
        return pct_correl_coeff

    def get_cov(self):
        pass
    
    def get_sharpe_rat(self):
        pass
    
    def get_beta(self):
        pass

    def get_j_alpha(self):
        pass
