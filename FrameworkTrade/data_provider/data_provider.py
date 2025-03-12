import MetaTrader5 as mt5
import pandas as pd
from typing import Dict
from datetime import datetime
from events.events import DataEvent
from queue import Queue

class DataProvider():
    
    def __init__(self,events_queue:Queue, symbol_list: list, timeframe:str):
        self.symbols:list = symbol_list
        self.timeframe:str = timeframe
        self.events_queue:Queue = events_queue
        
        #Creamos un diccionario para guardar el datime de la ultima vela para cada simbolo
        self.last_bar_datetime: Dict[str,datetime] = {symbol:datetime.min for symbol in self.symbols}        
        
    def _map_timeFrames(self, timeframe: str) ->int:
        timeframe_mapping = {
            '1min': mt5.TIMEFRAME_M1,
            '2min': mt5.TIMEFRAME_M2,                        
            '3min': mt5.TIMEFRAME_M3,                        
            '4min': mt5.TIMEFRAME_M4,                        
            '5min': mt5.TIMEFRAME_M5,                        
            '6min': mt5.TIMEFRAME_M6,                        
            '10min': mt5.TIMEFRAME_M10,                       
            '12min': mt5.TIMEFRAME_M12,
            '15min': mt5.TIMEFRAME_M15,
            '20min': mt5.TIMEFRAME_M20,                       
            '30min': mt5.TIMEFRAME_M30,                       
            '1h': mt5.TIMEFRAME_H1,                          
            '2h': mt5.TIMEFRAME_H2,                          
            '3h': mt5.TIMEFRAME_H3,                          
            '4h': mt5.TIMEFRAME_H4,                          
            '6h': mt5.TIMEFRAME_H6,                          
            '8h': mt5.TIMEFRAME_H8,                          
            '12h': mt5.TIMEFRAME_H12,
            '1d': mt5.TIMEFRAME_D1,                       
            '1w': mt5.TIMEFRAME_W1,                       
            '1M': mt5.TIMEFRAME_MN1,                       
        }
        
        try:
            return timeframe_mapping[timeframe]
        except:
            print("No es valido el timeframe",timeframe)
        
    #Recuperamos los datos de la ultima vela
    def get_latest_close_bar(self,symbol: str,timeframe:str) -> pd.Series:
        #Definir parametros
        tf = self._map_timeFrames(timeframe) # temporalidad
        from_position= 1 # ultima vela cerrada (la ultima esta oscilando es un 0)
        num_bars = 1 # numero de velas que nos traemos
        try:
            bars_np_array = mt5.copy_rates_from_pos(symbol, tf, from_position, num_bars)
            if mt5.symbol_info(symbol) is None : 
                print("Simbolo none", symbol)
                return pd.Series() #devolver serie vacia
            
            bars = pd.DataFrame(bars_np_array)
            
            # Convertimos la columna time a datetime y la hacemos el índice
            bars['time'] = pd.to_datetime(bars['time'], unit='s')
            bars.set_index('time', inplace=True)
            
          # Cambiamos nombres de columnas y las reorganizamos
            bars.rename(columns={'tick_volume': 'tickvol', 'real_volume': 'vol'}, inplace=True)
            bars = bars[['open', 'high', 'low', 'close', 'tickvol', 'vol', 'spread']]
            
            if bars.empty : return pd.Series() #devolver serie vacia
            else: return bars.iloc[-1] #devolver el ultimo de la serie
        except Exception as e:
            print(f"No se han recuperado los datos de la ultima vela {symbol} {timeframe}. MT5 error:{mt5.last_error()}, exception:{e}")
            
    #Recuperamos los datos de las ultimas n velas
    def get_latests_closes_bars(self,symbol: str,timeframe:str, n_bars: int = 1) -> pd.DataFrame:
        try:
            #Validaciones
            if mt5.symbol_info(symbol) is None : 
                print("Simbolo none", symbol)
                return pd.DataFrame() #devolver serie vacia
            
            #Definir parametros
            tf = self._map_timeFrames(timeframe) # temporalidad
            from_position= 1 # ultima vela cerrada (la ultima esta oscilando es un 0)
            num_bars = n_bars if n_bars > 0 else 1 # numero de velas que nos traemos
            
            #Convertir int a data time
            bars = pd.DataFrame(mt5.copy_rates_from_pos(symbol, tf,from_position, num_bars)) 
            bars.set_index('tie',inplace=True)#convertimos la columna time en indice
            
            #Cambiar nombres de columnas y reordenar
            bars.rename(columns={'tick_volumen':'tickvol','real_volumen':'vol'},inplace=True)
            bars = bars[['open','high','low','close','tickvol','vol','spread']]
            
            if bars.empty : return pd.Series() #devolver serie vacia
            else: bars.iloc[-1] #devolver el ultimo de la serie
        except Exception as e:
            print(f"No se han recuperado los datos de las velas {symbol} {timeframe}. MT5 error:{mt5.last_error()}, exception:{e}")
            
        else:
            return bars

    def get_lastest_tick(self, symbol: str) -> dict:
        try:
            tick = mt5.symbol_info_tick(symbol)
            if tick is None :
                print(f"No se ha podido recuperar el ultimo tick del simbolo",symbol)
                return {}
            
        except Exception as e:
            print(f"Algo falló al recuperar el ultimo tick {symbol}. MT5 {mt5.last_error()}") 
            
        else:
            return tick._asdict()  

    def check_for_new_data(self) -> None:
        #1) comprobar datos nuevos
        for symbol in self.symbols:
            #Acceder a sus último datos disponibles
            latest_bar = self.get_latest_close_bar(symbol,self.timeframe)
            
            if latest_bar is None: continue
            
            #Comprobar si hay datos nuevos
            if not latest_bar.empty and latest_bar.name > self.last_bar_datetime[symbol]:
                #Actualizar ultima vela recuperada
                self.last_bar_datetime[symbol] = latest_bar.name
                
                #Crear evento de datos
                data_event = DataEvent(symbol=symbol,data=latest_bar)
                
                #añadir evento a la cola de eventos
                self.events_queue.put(data_event)