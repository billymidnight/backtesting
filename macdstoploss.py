import backtrader as bt
import yfinance as yf
import matplotlib.pyplot as plt
import time

class MACDStrategy(bt.Strategy):
    params = (('fast_ema', 12), ('slow_ema', 26), ('signal_ema', 9), ('stop_loss_pct', 0.01))  # Stop loss at 1%

    def __init__(self):
        self.macd = bt.indicators.MACD(self.data.close, 
                                       period_me1=self.params.fast_ema, 
                                       period_me2=self.params.slow_ema, 
                                       period_signal=self.params.signal_ema)
        self.signal = self.macd.signal
        self.crossover = bt.indicators.CrossOver(self.macd.macd, self.signal)  
        self.buy_price = None  
    
    def next(self):
        if self.crossover > 0 and not self.position: 
            max_shares_to_buy = self.broker.getcash() // self.data.close[0]
            if max_shares_to_buy > 0:
                self.buy(size=max_shares_to_buy)
                self.buy_price = self.data.close[0]  
                #(f"Buy order placed at {self.data.close[0]} on {self.data.datetime.date(0)} for {max_shares_to_buy} shares")
                #time.sleep(2)

        elif self.crossover < 0 and self.position:
            self.sell(size=self.position.size)
            self.buy_price = None  
            #print(f"Sell order placed at {self.data.close[0]} on {self.data.datetime.date(0)} for {self.position.size} shares")
            #time.sleep(2)

        if self.position and self.buy_price:
            stop_loss_price = self.buy_price * (1 - self.params.stop_loss_pct)
            if self.data.close[0] < stop_loss_price:
                self.sell(size=self.position.size)
                self.buy_price = None 
                #print(f"Stop loss triggered. Sell order placed at {self.data.close[0]} on {self.data.datetime.date(0)}")
                #time.sleep(2)

tickerlist = ["AAPL", "GOOGL", "META", "NVDA", "NFLX", "AMZN", "MSFT", "LLY", "COST", "WMT", 
              "KO", "MCD", "PEP", "DHR", "TXN", "CAT", "PFE", "DIS", "UBER", "CRWD", "F", "TRGP", "HSY", "EXPE",
              "CRL", "LKQ", "QRVO", "AOS", "MGM", "CZR", "PG", "WRB", "ARE"]

tickerlist = ["SKYW", "HCKT", "AOUT", "BA", "ENVX", "INSM", "MUJ", "XRX", "HNST"]

counter = 0
totalendings = []

for ticker in tickerlist:
    cerebro = bt.Cerebro()

    data = bt.feeds.PandasData(dataname=yf.download(ticker, '2022-03-02', '2024-08-02'))
    cerebro.adddata(data)

    cerebro.addstrategy(MACDStrategy)  

    cerebro.broker.setcash(10000.0)

    print(f'Starting Portfolio Value for {ticker}: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print(f'Ending Portfolio Value for {ticker}: %.2f' % cerebro.broker.getvalue())
    totalendings.append(cerebro.broker.getvalue())

    figure = cerebro.plot(show=False)[0][0]
    figure.savefig(f'{ticker}_MACDStrategy.png')
    plt.close(figure)  

    counter += 1

avg = sum(totalendings) / len(totalendings)
print(f"Average ending bankroll: {avg}")
