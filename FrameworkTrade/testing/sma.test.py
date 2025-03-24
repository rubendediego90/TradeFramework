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
        # Señal de compra (long): smaQuick cruza por encima de smaSlow
        if self.smaQuick[-1] > self.smaSlow[-1] and self.smaQuick[-2] <= self.smaSlow[-2]:  
            self.position.close()  # Cerramos cualquier posición anterior
            self.buy()  # Abrimos una posición larga

        # Señal de venta (short): smaQuick cruza por debajo de smaSlow
        elif self.smaQuick[-1] < self.smaSlow[-1] and self.smaQuick[-2] >= self.smaSlow[-2]:
            self.position.close()  # Cerramos cualquier posición anterior
            self.sell()  # Abrimos una posición corta

# Cargar datos históricos desde Yahoo Finance
symbol = "ETH-USD"
data = yf.download(symbol, start="2025-01-24", end="2025-03-23", interval="5m")
data.columns = [col[0] for col in data.columns]

# Asegurarnos de que 'Date' es el índice
data.index = pd.to_datetime(data.index)

# Crear y ejecutar el backtest

bt = Backtest(data, EstrategiaCrucesMA)

#Ejecutamos el backtest
stats = bt.run()

#Vamos los resultados del backtest
print('stats',stats)
