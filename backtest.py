import pandas as pd
import numpy as np

def logger(ticker1, ticker2, zscore, profit, returns, trades, long_sma, short_sma, timeframe):
    with open("log.txt",'a',encoding = 'utf-8') as f:
        f.write('\n' + str(ticker1) + ',') # asset1
        f.write(str(ticker2) + ',') # asset2
        f.write(str(zscore) + ',') # Z-score
        f.write(str(profit) + ',') # Total profit or loss ($)
        f.write(str(returns) + ',') # Total returns (%)
        f.write(str(trades) + ',') # Amount of trades
        f.write(str(long_sma) + ',') # Long SMA
        f.write(str(short_sma) + ',') # Short SMA
        f.write(str(timeframe)) # 1m / 5m / 15m


def backtest(data, ticker1, ticker2, zscore, long_sma=60, short_sma=5, timeframe='1m'):

    ratios_df = pd.DataFrame(columns=['Ratio', '5d Ratio MA', '60d Ratio MA'])
    ratios_df.Ratio = data[ticker1] / data[ticker2]
    ratios_df[f'{short_sma}d Ratio MA'] = ratios_df.Ratio.rolling(window=short_sma, center=False).mean()
    ratios_df[f'{long_sma}d Ratio MA'] = ratios_df.Ratio.rolling(window=long_sma, center=False).mean()
    ratios_df[f'std_{long_sma}'] = ratios_df.Ratio.rolling(window=long_sma, center=False).std()
    ratios_df[f'zscore_{long_sma}_{short_sma}'] = (ratios_df[f'{short_sma}d Ratio MA'] - ratios_df[f'{long_sma}d Ratio MA'])/ratios_df[f'std_{long_sma}']

    signals = pd.DataFrame(columns=['buy', 'sell'], index = ratios_df.index)
    signals['buy'] = np.where(ratios_df[f'zscore_{long_sma}_{short_sma}'] < -zscore, -1, 0)
    signals['sell'] = np.where(ratios_df[f'zscore_{long_sma}_{short_sma}'] > zscore, 1, 0)

    signals = signals[((signals.buy == -1) & (signals.buy.shift(1) == 0)) | ((signals.sell == 1) & (signals.sell.shift(1) == 0))]
    signals = signals[(signals.buy.shift(1) != signals.buy) | (signals.sell.shift(1) != signals.sell)]

    signals['ratio'] = ratios_df.shift(1)['Ratio']
    signals[ticker1] = data[ticker1]
    signals[f'{ticker2} * ratio[-1]'] = data[ticker2]
    signals[f'{ticker2} * ratio[-1]'] *= signals.ratio

    # Check if we got at least ONE buy and ONE sell

    if (signals['buy'].sum() == 0) or (signals['sell'].sum() == 0) or (len(signals) == 0):
        text = 'NO TRADES FOR THIS PARAMETERS, TRY OTHER PARAMETERS'
        print(text)
        return

    # We check if signals starts with buy order and ends with sell order
    if signals.iloc[0]['sell'] > 0:
        signals = signals.iloc[1:]
    if signals.iloc[-1]['buy'] < 0:
        signals = signals.iloc[:-1]

    profit = {}
    stop_loss = -signals[ticker1].iloc[0] * 0.005

    # Running strategy
    for index_row in signals.index:
        # If strategy is start with buy order => ok, else drop the first row and start with buy order
        if signals.loc[index_row, 'buy'] == -1:
            buy = signals.loc[index_row, ticker1] - signals.loc[index_row, f'{ticker2} * ratio[-1]']
        elif signals.loc[index_row, 'sell'] == 1:
            sell = signals.loc[index_row, f'{ticker2} * ratio[-1]'] - signals.loc[index_row, ticker1]
            profit[index_row] = sell - buy  

    # Stop-loss implentation
    for key in profit:
        if profit[key] < 0:
            profit[key] = stop_loss
    
    total_profit = sum(profit.values())
    returns = (((total_profit)/signals.iloc[0,-2])*100).round(2)
    logger(ticker1=ticker1, ticker2=ticker2, zscore=zscore, profit=total_profit, 
                        returns=returns, trades=len(profit), long_sma=long_sma, short_sma=short_sma, timeframe=timeframe)
