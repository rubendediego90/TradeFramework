from platform_connector.platform_connector import PlatformConnector
from data_provider.data_provider import DataProvider
from trading_director.trading_director import TradingDirector
from signal_generator.signals.signal_ma_crossover import SignalMACrossover
from queue import Queue

if __name__ == "__main__":
   
   #Definición de variables necesarias para la estrategeia
   symbols = ['EURUSD','BTCUSD','XAUUSD']
   timeframe = '1min'
   fast_ma_period = 25
   slow_ma_period = 50
   
   #Creación cola de eventos principal
   events_queue = Queue()
   
   #Creación modulos principales
   CONNECT = PlatformConnector(symbol_list=symbols)
   DATA_PROVIDER = DataProvider(events_queue=events_queue,symbol_list=symbols, timeframe=timeframe)
   SIGNAL_GENERATOR = SignalMACrossover(events_queue=events_queue,
                                        data_provider=DATA_PROVIDER,
                                        timeframe=timeframe,
                                        fast_period=fast_ma_period,
                                        slow_period=slow_ma_period
                                        )
   
   #Creacjon del tradind directo y ejecucion del metodo principal
   TRADING_DIRECTOR = TradingDirector(events_queue=events_queue,data_provider=DATA_PROVIDER, signal_generator=SIGNAL_GENERATOR)
   TRADING_DIRECTOR.execute()
