import pandas as pd

def sma(array, period):
    series = pd.Series(array)
    return series.rolling(window=period).mean().values 

def ema(array, period):
    series = pd.Series(array)
    return series.ewm(span=period, adjust=False).mean().values