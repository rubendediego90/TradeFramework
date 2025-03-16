from enum import Enum
from pydantic import BaseModel
import pandas as pd

class EventType(str,Enum):
    DATA = "DATA"
    SIGNAL = "SIGNAL"
    SIZING = "SIZING"
    
class SignalType(str,Enum):
    BUY = "BUY"
    SELL = "SELL"
    
class OrderType(str,Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    
class BaseEvent(BaseModel):
    event_type: EventType
    class Config:
        arbitrary_types_allowed=True
    
class DataEvent(BaseEvent):
    event_type: EventType = EventType.DATA
    symbol:str
    data:pd.Series
    
class SignalEvent(BaseEvent):
    event_type: EventType = EventType.SIGNAL
    symbol:str
    signal: SignalType                          # Compra o venta
    target_order: OrderType = OrderType.MARKET  # pendiente o a mercado
    target_price: float
    magic_number:int                            #id de estrategia
    sl:float                                    #por si necesitamos poner el cierre de velas anteriores 
    tp:float
    
class SizeEvent(BaseEvent):
    event_type: EventType = EventType.SIZING
    symbol:str
    signal: SignalType                          # Compra o venta
    target_order: OrderType = OrderType.MARKET  # pendiente o a mercado
    target_price: float
    magic_number:int                            #id de estrategia
    sl:float                                    #por si necesitamos poner el cierre de velas anteriores 
    tp:float
    volume:float                                   #volumen 
