import reader
import backtest


tickers = reader.get_tickers()


for ticker1, path1 in zip(tickers[0], tickers[1]):
    for ticker2, path2 in zip(tickers[0], tickers[1]):
        if ticker1 == ticker2:
            break
        else: 
            print(ticker1, path1)
            print(ticker2, path2, '\n')

            data = reader.read_files(ticker1, ticker2, path1, path2, start='2021-01-01 00:00:00')
            for sma_short in range(3, 15, 3):
                for sma_long in range(45, 90, 5):
                    for zscore in range(50, 200, 10):
                        zscore = (zscore/100)
                        backtest.backtest(data, ticker1, ticker2, zscore, sma_long, sma_short)

            print('Completed')
