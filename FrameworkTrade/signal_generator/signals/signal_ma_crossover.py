from ..interfaces.interface_signal_generator import ISignalGenerator
from events.events import DataEvent
from queue import Queue
from data_provider.data_provider import DataProvider
from events.events import SignalEvent
import pandas as pd

class SignalMACrossover(ISignalGenerator):
    
    def __init__(self,events_queue: Queue, data_provider:DataProvider,timeframe:str,fast_period:int,slow_period:int):
        self.events_queue = events_queue
        self.DATA_PROVIDER = data_provider
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.timeframe = timeframe
        
        if self.fast_period >= self.slow_period:
            raise Exception(f"ERROR: el periodo rapido {self.fast_period} es mayor o igual al lento {self.slow_period} SignalMACrossover", )
        
    def _create_and_put_signal_event(self,symbol: str, signal: str, target_order:str,target_price: float, magic_number:int, sl: float,tp: float) -> None:
        #Crear signal event
        signal_event = SignalEvent(symbol=symbol,
                                    signal=signal,
                                    target_order=target_order,
                                    target_price=target_price,
                                    magic_number=magic_number,
                                    sl=sl,
                                    tp=tp)
        
        #Añadir el signal event en la cola de eventos.
        self.events_queue.put(signal_event)
        
        
    
    def generate_signal(self,data_event:DataEvent) -> None:
        #Coger simbolo del evento
        symbol = data_event.symbol
        #recuperar los datos necesarios
        bars = self.DATA_PROVIDER.get_latests_closed_bars(symbol,self.timeframe,self.slow_period) # pasamos el mayor porque con mas velas luego traemos menos
        
        #Calcular el valor de los indicadores
        fast_ma = bars['close'][-self.fast_period:].mean()
        slow_ma = bars['close'].mean()
        
        #Detectar una señal de compra
        if fast_ma > slow_ma:
            signal = "BUY"
            
        elif slow_ma > fast_ma:
            signal = "SELL"
            
        
        else: signal = ""
        
    # Si tenemos señal, generamos SignalEvent y lo colocamos en la cola de Eventos
        if signal != "":
            self._create_and_put_signal_event(symbol=symbol,
                                                signal=signal,
                                                target_order="MARKET",
                                                target_price=0,
                                                magic_number=1234,
                                                sl=0.0,
                                                tp=0.0)