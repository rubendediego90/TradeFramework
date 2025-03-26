from enum import Enum

class SYMBOL(str,Enum):
    ORO = "GC=F"
    PLATA = "SI=F"
    PETROLEO = "CL=F"
    BTC = "BTC-USD"
    ETH = "ETH-USD"
    DAX = "^GDAXI"
    SP500 = "^GSPC"
    NASDAQ = "^IXIC"
    LIBRA_USD = "GBPUSD=X"
    EURO_USD = "EURUSD=X"
    
class TIMES_BARS(str,Enum):
    MIN_5 = "5m"
    H_1 = "1h"
    

