import pandas as pd
import yfinance as yf
import os
from datetime import datetime, timedelta

def download_data(symbol, time_bars,file_name, date_ini, date_end):
    """
    Función para descargar los datos de Yahoo Finance y guardarlos en un archivo CSV.
    """
    print("Descargando nuevos datos desde Yahoo Finance...")
    data = yf.download(symbol, start=date_ini, end=date_end, interval=time_bars)
    data.columns = [col[0] for col in data.columns]
    
    # Eliminar 'Adj Close' si no es necesario
    data = data[['Open', 'High', 'Low', 'Close', 'Volume']]  # Solo mantener las columnas necesarias
    
    data.index = pd.to_datetime(data.index)  # Asegurarse de que las fechas sean correctas
    data.index = data.index.tz_localize(None)  # Eliminar cualquier zona horaria (UTC)
    
    data.to_csv(file_name)
    return data

def getData(symbol, time_bars, file_name, date_ini=None, date_end=None, auto_date=True):
    """
    Método para obtener los datos de Yahoo Finance o cargar desde un archivo CSV.
    Si el archivo tiene más de 12 horas, lo descarga de nuevo.
    """
    
    if auto_date:
        # Si no se proporciona `date_ini`, se asigna la fecha actual
        if date_ini is None:
            date_ini = (datetime.today() - timedelta(days=59)).strftime('%Y-%m-%d')  # 59 días atrás
        # Si no se proporciona `date_end`, se asigna la fecha actual
        if date_end is None:
            date_end = datetime.today().strftime('%Y-%m-%d')
    
    # Verificar si el archivo existe
    if os.path.exists(file_name):
        # Obtener la fecha de creación del archivo
        file_creation_time = datetime.fromtimestamp(os.path.getmtime(file_name))
        time_diff = datetime.now() - file_creation_time

        # Si el archivo tiene más de 12 horas, descargamos los nuevos datos
        if time_diff > timedelta(hours=12):
            print(f"El archivo ha pasado más de 12 horas (última actualización hace {time_diff}), descargando nuevos datos...")
            return download_data(symbol, date_ini, date_end, time_bars, file_name)
        else:
            print(f"Cargando datos desde el archivo existente (última actualización hace {time_diff})...")
            # Cargar los datos desde el archivo CSV, omitiendo cualquier fila no válida
            data = pd.read_csv(file_name, index_col=0, parse_dates=True)

            # Filtrar cualquier fila que no tenga un índice de fecha válido
            data = data[pd.to_datetime(data.index, errors='coerce').notna()]

            # Asegurarse de solo tener las columnas necesarias
            data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
            
            # Eliminar la zona horaria de las fechas
            data.index = data.index.tz_localize(None)
            
            # Asegurarnos de que 'Date' es el índice
            data.index = pd.to_datetime(data.index)
            
            return data
    else:
        # Si no existe el archivo, descargamos los datos
        print("El archivo no existe, descargando nuevos datos...")
        return download_data(symbol, date_ini, date_end, time_bars, file_name)


