"""
The script shows picks over parameters to find the best suitable for strategy

Source: Yahoo Finance

"""

tickers = [
    'BTC-USD', 'ETH-USD', 'BNB-USD', 'SOL1-USD', 'ADA-USD', 'XRP-USD', 'DOT1-USD', 'LUNA1-USD', 'DOGE-USD', 'AVAX-USD'
]

import yfinance as yf
import pandas as pd
start = '2021-11-15'
end = '2021-12-15'

data = yf.download(tickers, start, end, interval='15m')['Adj Close']
from backtest import backtest


for x in range(len(tickers)):
    for y in range(len(tickers)):
        if x == y:
            break
        elif tickers[x] != tickers[y]:
            if data[tickers[x]][0] < data[tickers[y]][0]:
                a = tickers[x]
                b = tickers[y]
                tickers[y] = a
                tickers[x] = b

            for posible_zscores in range(50, 200, 5):
                posible_zscores = (posible_zscores/100)
                for short_sma in range(3, 15, 3):
                    for long_sma in range(30, 150, 10):
                        try:
                            backtest(data[[tickers[x], tickers[y]]], tickers[x], tickers[y],
                                    zscore=posible_zscores, long_sma=long_sma, short_sma=short_sma, timeframe='15m')
                            print(tickers[x], tickers[y], posible_zscores,
                                    long_sma, short_sma)
                        except: pass