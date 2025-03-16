from ..interfaces.interface_position_sizer import IPositionSizer
import MetaTrader5 as mt5

class MinSizePositionSizer(IPositionSizer):
    
    def size_signal(self, signaL_event, data_provider) -> float:
        #Devolver el minimo de tamaño de operacion
        volume = mt5.symbol_info(signaL_event.symbol).volume_min
        if volume is not None:
            return volume
        else:
            print(" (MinSizePositionSizer) No se ha podido determinar el volumen minimo para el instrumento")
            return 0.0 #0 para que no opere