from platform_connector.platform_connector import PlatformConnector
from data_provider.data_provider import DataProvider
from trading_director.trading_director import TradingDirector
from signal_generator.signals.signal_ma_crossover import SignalMACrossover
from queue import Queue
from position_sizer.position_sizer import PositionSizer
from position_sizer.properties.position_sizer_properties import MinSizingProps, FixedSizingProps

if __name__ == "__main__":
   
   #Definición de variables necesarias para la estrategeia
   symbols = ['EURUSD','USDJPY','XAUUSD']
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
   
   POSITION_SIZER = PositionSizer(events_queue=events_queue,
                                  data_provider=DATA_PROVIDER,
                                  sizing_properties=FixedSizingProps(volume=0.076))
   
   #Creacjon del tradind directo y ejecucion del metodo principal
   TRADING_DIRECTOR = TradingDirector(events_queue=events_queue,data_provider=DATA_PROVIDER, signal_generator=SIGNAL_GENERATOR,position_sizer=POSITION_SIZER)
   TRADING_DIRECTOR.execute()
