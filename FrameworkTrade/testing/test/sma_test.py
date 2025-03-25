# python -m testing.test.sma_test

import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover,plot_heatmaps
from testing.utils.data_utils import getData
from testing.utils.indicadores_utils import sma
# import sambo


def optimizeFunc(series):
    if series['# Trades'] < 10:
        return -1 #
    '''

    if series['Win Rate [%]'] < 60:
        return -1 #
    '''
    return series["Profit Factor"]
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
    #date_ini = "2025-01-25"
    #date_end = "2025-03-25"
    #************************
    #print(sambo.__version__)
    # Obtener los datos
    file_name = f"data_{symbol}.csv"
    data = getData(symbol, time_bars, file_name)

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
    ''',optimize_result''' 
    stats, heatmap = bt.optimize(
    sma_quick_data=range(110,120,1),
    sma_slow_data=range(130,140,1),
    stop_loss=[0.9],
    maximize=optimizeFunc,
    #maximize='Return [%]',
    # method='sambo',
    return_heatmap=True,
    # return_optimization=True
    )
    
    plot_heatmaps(heatmap)
    # print('sambo',optimize_result)
    
    
    # print('Resultados de la optimización:', stats_op)
    
    #result = stats_op["_strategy"]
    # print('resultado optimizacion',result)
    #stats['_trades'] 
    #print('_trades',stats_op["_trades"])
    
    #result_heat_map = heatmap.sort_values().iloc[-20:]
    
    #result_heat_map = heatmap.sort_values().iloc[-20:]
    #result_heat_map.to_csv("result_heat_map.csv", index=False)
    heatmap.to_csv("result_heat_map.csv", index=False)
