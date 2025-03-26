# python -m testing.test.sma_test

import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from testing.utils.data_utils import getData
from testing.utils.indicadores_utils import sma
from testing.utils.optimize_utils import Optimizer
from testing.types.types import SYMBOL,TIMES_BARS

class EstrategiaCrucesMA(Strategy):
    sma_quick_data=200
    sma_slow_data=275
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
    symbol = SYMBOL.LIBRA_USD
    symbol_casted = SYMBOL.LIBRA_USD.name_str
    time_bars = TIMES_BARS.MIN_5
    #************************
    
    # Obtener los datos
    file_name = f"data_{symbol}.csv"
    data = getData(symbol, time_bars, file_name)

    # Crear y ejecutar el backtest
    bt = Backtest(data, EstrategiaCrucesMA, exclusive_orders=True, cash=10000000000000000)
    
    # Ejecutar el backtest
    stats = bt.run()

    # Ver los resultados del backtest
    print(stats)
    
    # Optimizar

    optimizer = Optimizer(bt, symbol_casted=symbol_casted,name_strategy="SMA",text="Hola el resuemne de la prueba esta bien hecho")
    optimizer.run()
    #optimizer.set_folder_name(symbol_casted,'SMA')

