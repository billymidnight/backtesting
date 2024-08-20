import backtrader as bt
import yfinance as yf
import matplotlib.pyplot as plt

class BollingerBandsBreakoutStrategy(bt.Strategy):
    params = (('period', 20), ('devfactor', 2), ('threshold', 0.1))  # 20% threshold by default

    def __init__(self):
        self.boll = bt.indicators.BollingerBands(self.data.close, 
                                                 period=self.params.period, 
                                                 devfactor=self.params.devfactor)
        self.bandwidth = self.boll.lines.top - self.boll.lines.bot  # Difference between top and bottom bands
        self.sma_bandwidth = bt.indicators.SimpleMovingAverage(self.bandwidth, period=self.params.period)
        self.in_position = False
    
    def next(self):
        bandwidth_change = (self.bandwidth[0] - self.sma_bandwidth[0]) / self.sma_bandwidth[0]

        if not self.in_position and bandwidth_change > self.params.threshold and self.data.close > self.boll.lines.top:
            self.buy(size=9)
            self.in_position = True
            #print(f"Buy order placed at {self.data.close[0]} on {self.data.datetime.date(0)}")
        
        elif self.in_position and bandwidth_change < -self.params.threshold:
            self.sell(size=9)
            self.in_position = False
            #print(f"Sell order placed at {self.data.close[0]} on {self.data.datetime.date(0)}")

tickerlist = ["AAPL", "GOOGL", "META", "NVDA", "NFLX", "AMZN", "MSFT", "LLY", "COST", "WMT", 
              "KO", "MCD", "PEP", "DHR", "TXN", "CAT", "PFE", "DIS", "UBER", "CRWD", "F", "TRGP", "HSY", "EXPE",
              "CRL", "LKQ", "QRVO", "AOS", "MGM", "CZR", "PG", "WRB", "ARE"]
totalendings = []
counter = 0

for ticker in tickerlist:
    cerebro = bt.Cerebro()

    data = bt.feeds.PandasData(dataname=yf.download(ticker, '2018-10-02', '2024-08-02'))
    cerebro.adddata(data)

    cerebro.addstrategy(BollingerBandsBreakoutStrategy)

    cerebro.broker.setcash(10000.0)

    print(f'Starting Portfolio Value for {ticker}: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print(f'Ending Portfolio Value for {ticker}: %.2f' % cerebro.broker.getvalue())
    totalendings.append(cerebro.broker.getvalue())

    counter += 1

avg = sum(totalendings) / len(totalendings)
print(f"Average ending bankroll: {avg}")
