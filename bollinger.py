import backtrader as bt
import yfinance as yf
import matplotlib.pyplot as plt

class BollingerBandsStrategy(bt.Strategy):
    params = (('period', 20), ('devfactor', 2), ('ema_period', 250))

    def __init__(self):
        self.boll = bt.indicators.BollingerBands(self.data.close, 
                                                 period=self.params.period, 
                                                 devfactor=self.params.devfactor)
        self.ema200 = bt.indicators.ExponentialMovingAverage(self.data.close, period=self.params.ema_period)
        self.crossunder = bt.indicators.CrossOver(self.data.close, self.boll.lines.bot)
        self.crossover = bt.indicators.CrossOver(self.data.close, self.boll.lines.top)
    
    def next(self):
        if self.crossunder < 0 and self.data.close > self.ema200:
            self.buy(size=5)
        
        elif self.crossover > 0:
            if self.position:
                self.sell(size=5)

tickerlist = ["AAPL", "GOOGL", "META", "NVDA", "NFLX", "AMZN", "MSFT", "LLY", "COST", "WMT", 
              "KO", "MCD", "PEP", "DHR", "TXN", "CAT", "PFE", "DIS", "UBER", "CRWD", "F", "TRGP", "HSY", "EXPE",
              "CRL", "LKQ", "QRVO", "AOS", "MGM", "CZR", "PG", "WRB", "ARE"]
totalendings = []
counter = 0

for ticker in tickerlist:
    cerebro = bt.Cerebro()

    data = bt.feeds.PandasData(dataname=yf.download(ticker, '2018-10-02', '2024-08-02'))
    cerebro.adddata(data)

    cerebro.addstrategy(BollingerBandsStrategy)

    cerebro.broker.setcash(10000.0)

    print(f'Starting Portfolio Value for {ticker}: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print(f'Ending Portfolio Value for {ticker}: %.2f' % cerebro.broker.getvalue())
    totalendings.append(cerebro.broker.getvalue())

    # figure = cerebro.plot(show=False)[0][0]
    # figure.savefig(f'{ticker}_BollingerBandsStrategy.png')
    # plt.close(figure)  

    counter += 1

avg = sum(totalendings) / len(totalendings)
print(f"Average ending bankroll: {avg}")
