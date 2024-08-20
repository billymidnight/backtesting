import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import time

bankroll = 10000
equityhistory = []
holdshares = 0
t = 0

aapl_data = yf.download('GOOGL', start='2018-08-02', end='2024-08-09')
sma_20 = []
upper_band = []
lower_band = []

for i in range(len(aapl_data)):
    if i < 20:
        sma = np.mean(aapl_data['Close'].iloc[:i+1])  
    else:
        sma = np.mean(aapl_data['Close'].iloc[i-19:i+1])
    std_dev = np.std(aapl_data['Close'].iloc[i-19:i+1]) if i >= 19 else np.std(aapl_data['Close'].iloc[:i+1])
    price = aapl_data['Close'].iloc[i]
    if (i > 0):
        price_prev = aapl_data['Close'].iloc[i-1]
    sma_20.append(sma)
    upper_band.append(sma + 1.9 * std_dev)
    lower_band.append(sma - 1.9 * std_dev)


    ## IMPLEMENTING BOLLINGER ##

    if (t > 35):
        if (price_prev > lower_band[-2] and price <= lower_band[-1] and holdshares == 0):
            buyamount = 0.75 * bankroll
            sharestobuy = buyamount // price
            bankroll -= sharestobuy * price
            holdshares += sharestobuy
            print(f"Placed buy order for AAPL at price: ${price} on {aapl_data.index[i].date()}. New bankroll: ${bankroll}")
            #time.sleep(2)
        elif (price_prev < upper_band[-2] and price >= upper_band[-1] and holdshares > 0):
            sharestosell = holdshares
            holdshares -= sharestosell
            bankroll += sharestosell * price
            print(f"Placed sell order for AAPL at price: ${price} on {aapl_data.index[i].date()}. New bankroll: ${bankroll}")
            #time.sleep(2)



    print(f"Date: {aapl_data.index[i].date()}, Close Price: {aapl_data['Close'].iloc[i]:.2f}")
    print(f"Upper Band: {upper_band[-1]:.2f} | Lower Band: {lower_band[-1]:.2f} | Price: {aapl_data['Close'].iloc[i]:.2f}")

    time.sleep(0.0001)
    
    equityhistory.append(bankroll + holdshares * price)
    t = t + 1

sma_20 = np.array(sma_20)
upper_band = np.array(upper_band)
lower_band = np.array(lower_band)

plt.figure(figsize=(14, 7))
plt.plot(aapl_data['Close'], label='Closing Prices', color='blue')
plt.plot(aapl_data.index, sma_20, label='SMA 20', color='orange', linestyle='--')
plt.plot(aapl_data.index, upper_band, label='Upper Band', color='green')
plt.plot(aapl_data.index, lower_band, label='Lower Band', color='red')
plt.fill_between(aapl_data.index, lower_band, upper_band, color='lightgray', alpha=0.3)
plt.title('AAPL Closing Prices and Bollinger Bands')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend(loc='upper left')
plt.show()


print(equityhistory[-1])

plt.figure(figsize=(14, 7))
plt.plot(aapl_data.index, equityhistory, label='Equity', color='blue', marker='o')
plt.title('Equity Over Time')
plt.xlabel('Date')
plt.ylabel('Equity')
plt.legend(loc='upper left')
plt.show()
plt.savefig('equity.png')