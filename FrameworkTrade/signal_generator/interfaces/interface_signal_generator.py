from typing import Protocol
from events.events import DataEvent

class ISignalGenerator(Protocol):
    
    def generate_signal(self,datata_event:DataEvent) -> None: ...
