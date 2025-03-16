from typing import Protocol
from events.events import SignalEvent
from data_provider.data_provider import DataProvider

class IPositionSizer(Protocol):
    #da el tamaño a una señal
    def size_signal(self,signaL_event:SignalEvent, data_provider:DataProvider) -> float: ...