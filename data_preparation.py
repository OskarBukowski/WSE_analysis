import pandas as pd
import pandas_datareader.data as web
import numpy as np


class Data:

    SESSIONS = 252
    RFR = 0.01/252
    ALPHA = 1


    def __init__(self, ticker_input):
        self.ticker_input = ticker_input
        self.market_data = None

    def market_data_from_stooq(self):
        self.market_data = web.DataReader(f"{self.ticker_input}.PL", 'stooq')
        self.market_data = self.market_data.drop(columns=['Open', 'High', 'Low'])
        self.market_data['Delta'] = self.market_data['Close'].pct_change()
        self.market_data['Date'] = pd.to_datetime(self.market_data.index)
        self.market_data = self.market_data.set_index('Date', drop=True)

        return self.market_data



    def statistics(self):

        self.log_returns = np.log(self.market_data_from_stooq()['Close']/self.market_data_from_stooq()['Close'].shift(1)).fillna(method='backfill')

        self.annualized_std = round(self.log_returns.std() * np.sqrt(252), 4)
        self.mean = round(self.log_returns.mean(), 4)
        self.skewness = round(self.log_returns.skew(), 4)
        self.kurtosis = round(self.log_returns.kurtosis(), 4)
        self.max_value = round(self.log_returns.max(), 4)
        self.min_value = round(self.log_returns.min(), 4)

        return self.log_returns, self.annualized_std, self.mean, self.skewness, self.kurtosis, self.max_value, self.min_value

    def financial_metrics_single(self):

        self.trailing_volatility = self.statistics()[0].rolling(window=14).std() * np.sqrt(Data.SESSIONS)

        self.mean_return = self.statistics()[0].rolling(window=14).mean()
        self.sharpe_ratio = (self.mean_return - Data.RFR) * Data.SESSIONS / self.trailing_volatility

        sortino_vol = self.statistics()[0][self.statistics()[0] < 0].rolling(window=Data.SESSIONS, center=True,
                                                                     min_periods=5).std() * np.sqrt(Data.SESSIONS)
        self.sortino_ratio = (self.mean_return - Data.RFR) * Data.SESSIONS / sortino_vol

        return self.trailing_volatility, self.mean_return, self.sharpe_ratio, self.sortino_ratio


    def financial_metrics_with_benchmark(self):

        benchmark_data = web.DataReader('WIG20.PL', 'stooq')
        benchmark_data = benchmark_data.drop(columns=['Open', 'High', 'Low'])

        log_bench_returns = np.log(benchmark_data.Close / benchmark_data.Close.shift(1)).fillna(method='backfill')
        benchmark_vol = log_bench_returns.rolling(window=14).std() * np.sqrt(Data.SESSIONS)


        self.m2_ratio = (self.financial_metrics_single()[2] * benchmark_vol / Data.SESSIONS + Data.RFR) * Data.SESSIONS
        self.returns = self.market_data_from_stooq()['Delta'].dropna()

        return self.m2_ratio, self.returns



    def max_drawdown(self):
        cumulative_returns = (1 + self.returns).cumprod()
        peak = cumulative_returns.expanding(min_periods=1).max()
        self.drawdown = (cumulative_returns / peak) - 1

        return self.drawdown.min()




    def historicalVAR(self):
        if isinstance(self.statistics()[0], pd.Series):
            return np.percentile(self.financial_metrics_with_benchmark()[1], Data.ALPHA)

        elif isinstance(self.statistics()[0], pd.DataFrame):
            return self.financial_metrics_with_benchmark()[1].aggregate(self.historicalVAR, Data.ALPHA)

        else:
            raise TypeError('Expected returns to be dataframe or series')


    def historicalCVAR(self):
        if isinstance(self.financial_metrics_with_benchmark()[1], pd.Series):
            belowVAR = self.financial_metrics_with_benchmark()[1] <= self.historicalVAR()
            return self.financial_metrics_with_benchmark()[1][belowVAR].mean()

        elif isinstance(self.financial_metrics_with_benchmark()[1], pd.DataFrame):
            return self.financial_metrics_with_benchmark()[1].aggregate(self.historicalCVAR, Data.ALPHA)

        else:
            raise TypeError('Expected returns to be dataframe or series')


    def calmar_ratio(self):
        return np.exp(self.statistics()[0].mean() * 252) / abs(self.max_drawdown())






