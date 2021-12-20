import pandas as pd
import web_scrapping
import tkinter_input
import pandas_datareader.data as web
import numpy as np

gpw_ticker = "KPL"


class Data:

    SESSIONS = 252
    RFR = 0.01/252
    ALPHA = 1


    def __init__(self, ticker_input):
        self.ticker_input = tkinter_input.Execute.user_tkinter_input

    def market_data_from_stooq(self):

        market_data = web.DataReader(f"{self.ticker_input}.PL", 'stooq')
        market_data = market_data.drop(columns=['Open', 'High', 'Low'])
        market_data['Delta'] = market_data['Close'].pct_change()
        market_data['Date'] = pd.to_datetime(market_data.index)
        market_data = market_data.set_index('Date', drop=True)
        self.market_data = market_data

        return market_data

    def statistics(self):

        self.log_returns = np.log(self.market_data.Close / self.market_data.Close.shift(1)).fillna(method='backfill')

        self.annualized_std = round(self.log_returns.std() * np.sqrt(252), 4)
        self.mean = round(self.log_returns.mean(), 4)
        self.skewness = round(self.log_returns.skew(), 4)
        self.kurtosis = round(self.log_returns.kurtosis(), 4)
        self.max_value = round(self.log_returns.max(), 4)
        self.min_value = round(self.log_returns.min(), 4)

    def financial_metrics_single(self):

        self.trailing_volatility = self.log_returns.rolling(window=Data.SESSIONS).std() * np.sqrt(Data.SESSIONS)

        self.mean_return = self.log_returns.rolling(window=Data.SESSIONS).mean()
        self.sharpe_ratio = (self.mean_return - Data.RFR) * 252 / self.trailing_volatility

        sortino_vol = self.log_returns[self.log_returns < 0].rolling(window=Data.SESSIONS, center=True,
                                                                     min_periods=5).std() * np.sqrt(Data.SESSIONS)
        self.sortino_ratio = (self.mean_return - Data.RFR) * 252 / sortino_vol


    def financial_metrics_with_benchmark(self):

        benchmark_data = web.DataReader('WIG20.PL', 'stooq')
        benchmark_data = benchmark_data.drop(columns=['Open', 'High', 'Low'])

        log_bench_returns = np.log(benchmark_data.Close / benchmark_data.Close.shift(1)).fillna(method='backfill')
        benchmark_vol = log_bench_returns.rolling(window=Data.SESSIONS).std() * np.sqrt(Data.SESSIONS)


        self.m2_ratio = (self.sharpe_ratio * benchmark_vol / Data.SESSIONS + Data.RFR) * Data.SESSIONS
        self.returns = self.market_data.Close.pct_change().dropna()


        def max_drawdown(self):
            cumulative_returns = (1 + self.returns).cumprod()
            peak = cumulative_returns.expanding(min_periods=1).max()
            drawdown = (cumulative_returns / peak) - 1

            return drawdown.min()


        def historicalVAR(self):
            if isinstance(self.log_returns, pd.Series):
                return np.percentile(self.returns, Data.ALPHA)

            elif isinstance(self.log_returns, pd.DataFrame):
                return self.returns.aggregate(historicalVAR, Data.ALPHA)

            else:
                raise TypeError('Expected returns to be dataframe or series')


        def historicalCVAR(self):
            if isinstance(self.returns, pd.Series):
                belowVAR = self.returns <= historicalVAR(self.returns, Data.ALPHA)
                return self.returns[belowVAR].mean()

            elif isinstance(self.returns, pd.DataFrame):
                return self.returns.aggregate(historicalCVAR, Data.ALPHA)

            else:
                raise TypeError('Expected returns to be dataframe or series')


        drawdown = round((max_drawdown(self.returns) * 100), 4)

        calmar = round((np.exp(self.log_returns.mean() * 252) / abs(max_drawdown(self.returns))), 4)

        hist_var = round((historicalVAR(self.log_returns, Data.ALPHA)), 4)
        hist_cvar = round((historicalCVAR(self.log_returns, Data.ALPHA)), 4)
