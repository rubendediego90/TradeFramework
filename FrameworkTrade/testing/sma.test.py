import pandas as pd
import numpy as np
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import yfinance as yf

def sma(array, period):
    series = pd.Series(array)
    return series.rolling(window=period).mean().values 

class EstrategiaCrucesMA(Strategy):
    sma_quick_data=22
    sma_slow_data=112
    
    def init(self):
        self.smaQuick = self.I(sma, self.data.Close, self.sma_quick_data)
        self.smaSlow = self.I(sma, self.data.Close, self.sma_slow_data)

    def next(self):
        price = self.data.Close[-1]
        
        if crossover(self.smaSlow,self.smaSlow):
            self.buy(sl=price)
            
        elif crossover(self.smaSlow,self.smaQuick):
            self.sell()

#****   VARIABLES   *****
symbol = "ETH-USD"
time_bars = "5m"
date_ini = "2025-01-24"
date_end = "2025-03-23"
#************************

data = yf.download(symbol, start=date_ini, end=date_end, interval=time_bars)
data.columns = [col[0] for col in data.columns]

# Asegurarnos de que 'Date' es el índice
data.index = pd.to_datetime(data.index)

# Crear y ejecutar el backtest
bt = Backtest(data, EstrategiaCrucesMA,exclusive_orders=True) #con una orden nueva cierra las anteriores

#Ejecutamos el backtest
stats = bt.run()

#Vamos los resultados del backtest
print('stats',stats)
