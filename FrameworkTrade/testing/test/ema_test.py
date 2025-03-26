# python -m testing.test.ema_test

import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from testing.utils.data_utils import getData
from testing.utils.indicadores_utils import ema

def optimizeFunc(series):
    
    if series['# Trades'] < 10:
        return -1 
    '''
    if series['Win Rate [%]'] < 60:
        return -1 #
    '''
    
    return series["Profit Factor"]
class EstrategiaCruceema(Strategy):
    ema_quick_data=6
    ema_slow_data=237
    stop_loss = 0.80
    
    def init(self):
        self.emaQuick = self.I(ema, self.data.Close, self.ema_quick_data)
        self.emaSlow = self.I(ema, self.data.Close, self.ema_slow_data)

    def next(self):
        price = self.data.Close[-1]
        
        if crossover(self.emaQuick,self.emaSlow):
            stop_loss_price = self.stop_loss*price
            self.buy(sl=stop_loss_price) if stop_loss_price > 0 else self.buy()
            
        elif crossover(self.emaSlow,self.emaQuick):
            stop_loss_price = price * (1 + (1 - self.stop_loss)) 
            self.sell(sl=stop_loss_price) if stop_loss_price == price * 2  else self.sell()

if __name__ == '__main__':
    #****   VARIABLES   *****
    symbol = "CL=F"
    time_bars = "5m"
    #************************

    # Obtener los datos
    file_name = f"data_{symbol}.csv"
    data = getData(symbol, time_bars, file_name)

    # Backtest
    bt = Backtest(data, EstrategiaCruceema, exclusive_orders=True)
    stats = bt.run()
    print(stats)
    
    # print(stats["_trades"])

    # Optimizar
    stats_op = bt.optimize(
        ema_quick_data=range(1,299,1),
        ema_slow_data=range(2,300,1),
        stop_loss=[0.9, 0.93, 0.95],
        maximize=optimizeFunc
        #maximize='Win Rate [%]'
    )

    print('Resultados de la optimización:', stats_op)
    print('resultado optimizacion',stats_op["_strategy"])
    print('_trades',stats_op["_trades"])
    

    
    