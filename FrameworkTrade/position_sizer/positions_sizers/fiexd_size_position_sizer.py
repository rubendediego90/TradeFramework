from ..interfaces.interface_position_sizer import IPositionSizer
from data_provider.data_provider import DataEvent
from events.events import SignalEvent
from ..properties.position_sizer_properties import FixedSizingProps

class FixedSizePositionSizer(IPositionSizer):
    
    def __init__(self, properties: FixedSizingProps):
        self.fixed_volume = properties.volume
    
    def size_signal(self, signaL_event: SignalEvent, data_provider: DataEvent) -> float:
        #Devolver el tamaño de la posicion fija
        
        if self.fixed_volume >= 0.0:
            return self.fixed_volume
        else:
            return 0.0
