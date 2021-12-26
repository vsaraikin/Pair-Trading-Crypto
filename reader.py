"""
Simple reader of data

You can download data from https://www.cryptodatadownload.com/

Then put your csv file (or files) into the /data folder
"""



import os
from posix import listdir
import pandas as pd
import numpy as np


def get_tickers():
    current_path = os.path.dirname(__file__)
    data_path = current_path + '/data'
    all_files = listdir(data_path)
    tickers = []

    for element in all_files:
        tickers.append(element[-18:][:-11])
    return (tickers, all_files)

def read_files(ticker1, ticker2, file1, file2, start = '2021-01-01 00:00:00'):
    print('Read path', file1)
    print('Read path', file2)

    df1 = pd.read_csv(f'data/{file1}', low_memory=False, skiprows=1, header=0, index_col='date')['close'].loc[:start]
    df1.name = ticker1
    df2 = pd.read_csv(f'data/{file2}', low_memory=False,  skiprows=1, header=0, index_col='date')['close'].loc[:start]
    df2.name = ticker2
    data = pd.concat([df1, df2], axis=1).dropna()
    data = data.sort_index(ascending=True)
    return data


def comparing_pairs():
    coins = get_tickers()
    calculated = pd.DataFrame(index=coins[0], columns=coins[0])
    for x in calculated.index:
        for y in calculated.columns:
            if (x == y):
                calculated.loc[x,y] = np.nan
                break
            else:
                calculated.loc[y,x] = 'Completed'
    return calculated