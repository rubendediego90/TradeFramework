import pandas as pd

def sma(array, period):
    series = pd.Series(array)
    return series.rolling(window=period).mean().values 