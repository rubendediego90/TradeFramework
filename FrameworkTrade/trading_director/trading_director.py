from data_provider.data_provider import DataProvider
from signal_generator.interfaces.interface_signal_generator import ISignalGenerator
from events.events import DataEvent,SignalEvent
import queue
from typing import Dict, Callable
import time
from datetime import datetime

class TradingDirector():
    
    def __init__(self, events_queue: queue.Queue, data_provider : DataProvider, signal_generator:ISignalGenerator):
        self.events_queue : queue.Queue = events_queue
        
        #Referencia de los modulos
        self.data_provider : DataProvider = data_provider
        self.signal_generator : ISignalGenerator = signal_generator
        
        #Controlador de trading
        self.trading_controller: bool = True
        
        #Creacion del event handler
        self.event_handler: Dict[str, Callable] = {
            "DATA":self._handle_data_event,
            "SIGNAL":self._handle_signal_event
        }
        
    def _handle_data_event(self, event: DataEvent):
        #Gestionamos los eventos de dataEvent
        print(f"Recibido DATA EVENT {event.symbol} - último precio de cierre:{event.data.close} ")
        self.signal_generator.generate_signal(event)
        
    def _handle_signal_event(self, event: SignalEvent):
        #Procesar signal event
        print(f"Recibido SIGNAL EVENT {event.signal} para {event.symbol}")
        
        
    def date_print(self) -> str:
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")    #dd/mm/aa hh:mm:ss
        
    def execute(self) -> None:
        
        #Definicion bucle principal
        while self.trading_controller:
            try:
                event = self.events_queue.get(block=False) #se recupera el primero que entro false porque no queremos que se bloquee si esta vacia
                
            except queue.Empty:
                self.data_provider.check_for_new_data()
                
            else:
                if event is not None:
                    handler = self.event_handler.get(event.event_type)
                    handler(event)
                else:
                    self.trading_controller = False
                    print("error, evento nulo")
                    
            time.sleep(0.01)# se ejecuta cada segundo
        print("FIN")
        
    