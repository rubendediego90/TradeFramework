# python -m testing.test.sma_test

import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from testing.utils.data_utils import getData
from testing.utils.indicadores_utils import sma

def optimizeFunc(series):
    '''
    if series['# Trades'] < 10:
        return -1 #

    if series['Win Rate [%]'] < 60:
        return -1 #
    '''
    return series["Return [%]"]
class EstrategiaCrucesMA(Strategy):
    sma_quick_data=22
    sma_slow_data=112
    stop_loss=0.95
    
    def init(self):
        self.smaQuick = self.I(sma, self.data.Close, self.sma_quick_data)
        self.smaSlow = self.I(sma, self.data.Close, self.sma_slow_data)

    def next(self):
        price = self.data.Close[-1]
        
        if crossover(self.smaSlow,self.smaSlow):
            stop_loss_price = self.stop_loss*price
            self.buy(sl=stop_loss_price)
            
        elif crossover(self.smaSlow,self.smaQuick):
            stop_loss_price = price * (1 + (1 - self.stop_loss)) 
            self.sell(sl=stop_loss_price)

if __name__ == '__main__':
    #****   VARIABLES   *****
    symbol = "CL=F"
    time_bars = "5m"
    #date_ini = "2025-01-25"
    #date_end = "2025-03-25"
    #************************

    # Obtener los datos
    file_name = f"data_{symbol}.csv"
    data = getData(symbol, time_bars, file_name) #,date_ini, date_end

    # Crear y ejecutar el backtest
    bt = Backtest(data, EstrategiaCrucesMA, exclusive_orders=True)
    
    # Ejecutar el backtest
    stats = bt.run()

    # Ver los resultados del backtest
    # print(stats)
    # Optimizar
    '''
    stats_op = bt.optimize(
        sma_quick_data=range(1,299,1),
        sma_slow_data=range(2,300,1),
        stop_loss=[0.9, 0.93, 0.95],
        maximize=optimizeFunc
    )
    '''
    
    stats_op = bt.optimize(
    sma_quick_data=range(110,120,1),
    sma_slow_data=range(130,140,1),
    stop_loss=[0.9],
    #maximize=optimizeFunc
    maximize='Return [%]'
    )
    
    print('Resultados de la optimización:', stats_op)
    
    result = stats_op["_strategy"]
    # print('resultado optimizacion',result)
    stats['_trades'] 
    print('_trades',stats_op["_trades"])
    '''
    stats_op_filtered = stats_op[
        (stats_op['# Trades'] > 10) &
        (stats_op['Win Rate [%]'] > 0.6)
        
    ]
    
    stats_op_ordered = stats_op_filtered.sort_values(by='Return [%]',ascending=False).head(10)
    
    print('stats_op_ordered',stats_op_ordered)
    '''