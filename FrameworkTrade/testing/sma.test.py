import pandas as pd
import numpy as np
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import yfinance as yf

def sma(array, period):
    series = pd.Series(array)
    return series.rolling(window=period).mean().values  # Convertimos de nuevo a numpy array

class EstrategiaCrucesMA(Strategy):
    def init(self):
        self.sma50 = self.I(sma, self.data.Close, 50)   # SMA rápida
        self.sma200 = self.I(sma, self.data.Close, 200)  # SMA lenta

    def next(self):
        # Señal de compra (long): SMA50 cruza por encima de SMA200
        if self.sma50[-1] > self.sma200[-1] and self.sma50[-2] <= self.sma200[-2]:  
            self.position.close()  # Cerramos cualquier posición anterior
            self.buy()  # Abrimos una posición larga

        # Señal de venta (short): SMA50 cruza por debajo de SMA200
        elif self.sma50[-1] < self.sma200[-1] and self.sma50[-2] >= self.sma200[-2]:
            self.position.close()  # Cerramos cualquier posición anterior
            self.sell()  # Abrimos una posición corta

# Cargar datos históricos desde Yahoo Finance
symbol = "ETH-USD"
data = yf.download(symbol, start="2025-01-25", end="2025-03-23", interval="5m")

# Limpiar las columnas para que sean simples
data.columns = [col[0] for col in data.columns]

# Asegurarnos de que 'Date' es el índice
data.index = pd.to_datetime(data.index)

# Crear y ejecutar el backtest
bt = Backtest(data, EstrategiaCrucesMA)
#Ejecutamos el backtest
stats = bt.run()

#Vamos los resultados del backtest
print('stats',stats)
