# python -m testing.test.sma_test

import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from testing.utils.data_utils import getData
from testing.utils.indicadores_utils import sma
from testing.utils.optimize_utils import Optimizer
from testing.types.types import SYMBOL,TIMES_BARS,STRATEGIES

class EstrategiaCrucesMA(Strategy):
    sma_quick_data=206
    sma_slow_data=47
    stop_loss=0.9
    
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
    symbol = SYMBOL.DAX
    symbol_casted = SYMBOL.DAX.name_str
    time_bars = TIMES_BARS.MIN_5
    columns_csv_best= ['sma_quick', 'sma_slow', 'stop_loss', 'Profit Factor']
    comment_readme ="Hola el resuemne de la prueba esta bien hecho"
    name_strategy=STRATEGIES.SMA
    #************************
    
    # Obtener los datos
    file_name = f"data_{symbol}.csv"
    data = getData(symbol, time_bars, file_name)

    # Crear y ejecutar el backtest
    bt = Backtest(data, EstrategiaCrucesMA, exclusive_orders=True, cash=10000000000000000)
    
    # Ejecutar el backtest
    stats = bt.run()
    print(stats)
    
    # Optimizar
    optimizer = Optimizer(
        bt, 
        symbol_casted=symbol_casted,
        name_strategy=name_strategy,
        text=comment_readme,
        data=data,
        columns_csv_best=columns_csv_best)
    
    optimizer.run()

