from ..interfaces.interface_position_sizer import IPositionSizer
from data_provider.data_provider import DataProvider
from events.events import SignalEvent
from ..properties.position_sizer_properties import RiskPctSizingProps
import MetaTrader5 as mt5
from utils.utils import Utils

class RiskPctPositionSizer(IPositionSizer):
    
    def __init__(self, properties: RiskPctSizingProps):
        self.risk_pct = properties.risk_pct
    
    def size_signal(self, signaL_event: SignalEvent, data_provider: DataProvider) -> float:

        #Calculamos la posicion en funcion del riesgo
        if self.risk_pct <= 0.0:
            print("RiskPctPositionSizer - El porcentaje de riesto introducido no es valdo")
            return 0.0
        
        #revisar que el stop loss sea diferente de 0.
        if signaL_event.sl <=0.0:
            print("RiskPctPositionSizer - El valor del stop loss no es valido")
            return 0.0
        
        #Acceder a la informacion de la cuenta para obtener la divisa
        account_info = mt5.account_info()
        
        #Acceder a la información del simbolo para calcular el riesgo
        symbol_info = mt5.symbol_info(signaL_event.symbol)
        
        #Recuperamos el preio de entrada estimado
        if signaL_event.target_order == "MARKET":
            #Obtener ultimo precio disponible en el mercado
            last_tick = data_provider.get_lastest_tick(signaL_event.symbol)
            entry_price = last_tick['ask'] if signaL_event.signal == "BUY" else last_tick['bid']
            
        #Si es una orden pendiente (limit o stop en bingX activar) cogemos el precio del signal
        else:
            entry_price = signaL_event.target_price
            
        #Conseguir valores necesarios
        equity = account_info.account_info
        volume_step = symbol_info.symbol_info # Cambio minimo de volumen (el lote puede ir de 0.1 a 0.2 , el cambio es 0.1)
        tick_size = symbol_info.trade_tick_size #Tamaño del precio minimo que varia 1.005 a 1.006 el tamaño minimo es 0.001
        account_ccy = account_info.currency     #divisa de la cuenta
        symbol_profit_ccy = symbol_info.currency_profit #divisa del profit del simnolo
        contract_size = symbol_info.trade_contract_size    #tamaño del contrato de un lote
        
        #Calculos auxiliares
        tick_value_profit_ccy = contract_size * tick_size   #cantiad ganada o perrida por lote
        
        #Convertir el tick value en profit ccy del simbolo a la divisa de la cuenta
        tick_value_account_ccy = Utils.convert_currency_amount_to_another_currency(tick_value_profit_ccy,symbol_profit_ccy,account_ccy)
                
        #Calculo tamaño posicion
        '''
        video 66, min 2 #abs valro absoluto para compra y venta, explicacion en 67
        '''
        try:
            precio_distancia_en_ticksizers_enteros = int(abs(entry_price - signaL_event.sl) / tick_size) 
            monerary_risk = equity * self.risk_pct 
            volume = monerary_risk / (precio_distancia_en_ticksizers_enteros*tick_value_account_ccy) 
            volume = round(volume/volume_step)*volume_step #TODO recondear el volumen hacia abajo
        except Exception as e:
            print("Error al calcular la posicion segun el % de riesgo, Exception: {e}")
            return 0.0
        
        else:
            return volume
        