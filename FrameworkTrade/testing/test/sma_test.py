# python -m testing.test.sma_test

import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from testing.utils.data_utils import getData
from testing.utils.indicadores_utils import sma
from testing.utils.optimize_utils import Optimizer

class EstrategiaCrucesMA(Strategy):
    sma_quick_data=22
    sma_slow_data=112
    stop_loss=0.95
    
    def init(self):
        self.smaQuick = self.I(sma, self.data.Close, self.sma_quick_data)
        self.smaSlow = self.I(sma, self.data.Close, self.sma_slow_data)

    def next(self):
        price = self.data.Close[-1]
        
        if crossover(self.smaQuick,self.smaSlow):
            stop_loss_price = self.stop_loss*price
            self.buy(sl=stop_loss_price)
            
        elif crossover(self.smaSlow,self.smaQuick):
            stop_loss_price = price * (1 + (1 - self.stop_loss)) 
            self.sell(sl=stop_loss_price)

if __name__ == '__main__':
    #****   VARIABLES   *****
    symbol = "GC=F"
    time_bars = "5m"
    #************************
    
    # Obtener los datos
    file_name = f"data_{symbol}.csv"
    data = getData(symbol, time_bars, file_name)

    # Crear y ejecutar el backtest
    bt = Backtest(data, EstrategiaCrucesMA, exclusive_orders=True)
    
    # Ejecutar el backtest
    stats = bt.run()

    # Ver los resultados del backtest
    print(stats)
    
    # Optimizar

    optimizer = Optimizer(bt)
    optimizer.run()

