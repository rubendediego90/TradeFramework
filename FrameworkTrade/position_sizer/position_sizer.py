from .interfaces.interface_position_sizer import IPositionSizer
from events.events import SignalEvent, SizeEvent
from data_provider.data_provider import DataProvider
from queue import Queue
from .positions_sizers.min_size_positions_sizer import MinSizePositionSizer
from .positions_sizers.fiexd_size_position_sizer import FixedSizePositionSizer
from .positions_sizers.risk_pct_position_sizer import RiskPctPositionSizer
from .properties.position_sizer_properties import BaseSizerProps, MinSizingProps,FixedSizingProps, RiskPctSizingProps
import MetaTrader5 as mt5
class PositionSizer(IPositionSizer) :
    
    def __init__(self, events_queue:Queue,data_provider: DataProvider, sizing_properties:BaseSizerProps):
        self.events_queue = events_queue
        self.data_provider = data_provider
        self.position_sizing_method = self._get_position_sizing_method(sizing_properties)
        
    def _get_position_sizing_method(self,sizing_props:BaseSizerProps) -> IPositionSizer:
        if isinstance(sizing_props,MinSizingProps):
            return MinSizePositionSizer()
        elif  isinstance(sizing_props,FixedSizingProps):
            return FixedSizePositionSizer(properties=sizing_props)
        elif  isinstance(sizing_props,RiskPctSizingProps):
            return RiskPctPositionSizer(properties=sizing_props)
        
        else:
            raise Exception (f"ERROR metodo se sizing desconocido", sizing_props)
        
    
    def _create_and_put_sizing_event(self,signal_event:SignalEvent, volume: float) ->None:
        sizing_event = SizeEvent(symbol=signal_event.symbol,
                                   signal=signal_event.signal,
                                   target_order=signal_event.target_order,
                                   target_price=signal_event.target_price,
                                   magic_number=signal_event.magic_number,
                                   sl=signal_event.sl,
                                   tp=signal_event.tp,
                                   volume= volume)
        
        self.events_queue.put(sizing_event)
        
    def size_signal(self, signaL_event: SignalEvent) -> None:
        
        #Obtener el volumen adecuado segun el metodo de sizing
        volume = self.position_sizing_method.size_signal(signaL_event,self.data_provider)
        
        #Control de seguridad
        if volume < mt5.symbol_info(signaL_event.symbol).volume_min:
            print(f"El volumen {volume} es menor que el volumen admitido por el symbolo {signaL_event.symbol}")
            return
        
        #Colocar el sizing event en la queue
        self._create_and_put_sizing_event(signaL_event,volume=volume)