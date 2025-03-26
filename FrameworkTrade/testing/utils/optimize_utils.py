from backtesting.lib import plot_heatmaps

class Optimizer:
    def __init__(self, bt):
        self.bt = bt
        
    def optimizeFunc(self, series):
        if series['# Trades'] < 10:
            return -1 #
        '''

        if series['Win Rate [%]'] < 60:
            return -1 #
        '''
        return series["Profit Factor"]

    def run(self):
            '''
        stats_op = bt.optimize(
            sma_quick_data=range(1,299,1),
            sma_slow_data=range(2,300,1),
            stop_loss=[0.9, 0.93, 0.95],
            maximize=optimizeFunc
        )
        '''

            stats, heatmap = self.bt.optimize(
                sma_quick_data=range(112,120,1),
                sma_slow_data=range(132,140,1),
                stop_loss=[0.9],
                maximize=self.optimizeFunc,
                #maximize='Return [%]',
                return_heatmap=True
            )

            plot_heatmaps(heatmap)
            # print('sambo',optimize_result)
            
            heatmap_reset = heatmap.reset_index()

            # Si alguna columna no tiene nombre, asignamos nombres manualmente
            heatmap_reset.columns = ['sma_quick_data', 'sma_slow_data', 'stop_loss', 'Profit Factor']
            heatmap_reset = heatmap_reset.sort_values(by='Profit Factor', ascending=False)

            # Guardar el DataFrame en un archivo CSV sin el índice original
            heatmap_reset.to_csv('mi_data.csv', index=False)
            
            # print('Resultados de la optimización:', stats_op)
            
            #result = stats_op["_strategy"]
            # print('resultado optimizacion',result)
            #stats['_trades'] 
            #print('_trades',stats_op["_trades"])
    


