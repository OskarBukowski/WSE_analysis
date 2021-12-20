import pandas as pd
import web_scrapping
import tkinter_input
import pandas_datareader.data as web
import numpy as np

gpw_ticker = "KPL"


asset = web.DataReader("KPL.PL", 'stooq')
print(asset)

asset = asset.drop(columns = ['Open', 'High', 'Low'])
asset['Delta'] = asset['Close'].pct_change()
asset['Date'] = pd.to_datetime(asset.index)
asset = asset.set_index('Date', drop=True)



print(asset)




log_returns = np.log(asset.Close/asset.Close.shift(1)).fillna(method = 'backfill')
annualized_std = round(log_returns.std() * np.sqrt(252),4)
mean = round(log_returns.mean(), 4)
skewness = round(log_returns.skew(), 4)
kurtosis = round(log_returns.kurtosis(), 4)
max_value = round(log_returns.max(), 4)
min_value = round(log_returns.min(), 4)

print('Statistics measures')

print(log_returns)
print(annualized_std)
print(mean)
print(skewness)
print(kurtosis)
print(max_value)
print(min_value)





days = 252
trailing_volatility = log_returns.rolling(window = days).std() * np.sqrt(days)

print("trailing volatility", trailing_volatility)


rfr = 0.01 / 252  # daily risk free rate
mean_return = log_returns.rolling(window = days).mean()

print("mean_returns", mean_return)


sharpe_ratio = (mean_return - rfr) * 252 / trailing_volatility
sortino_vol = log_returns[log_returns<0].rolling(window = days, center = True, min_periods = 5).std()* np.sqrt(days)
sortino_ratio = (mean_return - rfr) * 252 / sortino_vol

bench = web.DataReader('WIG20.PL', 'stooq')
bench = bench.drop(columns = ['Open', 'High', 'Low'])


print("Financial metrics")

print(sharpe_ratio)
print(sortino_ratio)
print(bench)



log_bench_returns = np.log(bench.Close/bench.Close.shift(1)).fillna(method = 'backfill')
benchmark_vol = log_bench_returns.rolling(window = days).std() * np.sqrt(days)
m2_ratio = (sharpe_ratio*benchmark_vol/ days + rfr)* days

print(" Measures 2")

print(log_bench_returns)
print(benchmark_vol)
print(m2_ratio)



def max_drawdown(returns):
    cumulative_returns = (1 + returns).cumprod()
    peak = cumulative_returns.expanding(min_periods=1).max()
    drawdown = (cumulative_returns / peak) - 1

    return drawdown.min()


returns = asset.Close.pct_change().dropna()

drawdown = round((max_drawdown(returns) * 100), 4)

calmar = round((np.exp(log_returns.mean() * 252) / abs(max_drawdown(returns))), 4)


def historicalVAR(log_returns, alpha=1):
    if isinstance(log_returns, pd.Series):
        return np.percentile(returns, alpha)

    elif isinstance(log_returns, pd.DataFrame):
        return returns.aggregate(historicalVAR, alpha=1)

    else:
        raise TypeError('Expected returns to be dataframe or series')


def historicalCVAR(returns, alpha=1):
    if isinstance(returns, pd.Series):
        belowVAR = returns <= historicalVAR(returns, alpha=1)
        return returns[belowVAR].mean()

    elif isinstance(returns, pd.DataFrame):
        return returns.aggregate(historicalCVAR, alpha=1)


    else:
        raise TypeError('Expected returns to be dataframe or series')


hist_var = round((historicalVAR(log_returns, alpha=1)), 4)
hist_cvar = round((historicalCVAR(log_returns, alpha=1)), 4)
