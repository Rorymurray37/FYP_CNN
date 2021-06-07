import pandas as pd
import talib as ta
import os
from datetime import datetime

def prepareData(df):
    df['DateTime'] = df[['Date','Time']].apply(lambda x : '{}{}'.format(x[0],x[1]), axis=1) # combine columns
    df['DateTime'] = pd.to_datetime(df['DateTime'],format = '%Y%m%d%H%M%S')
    df.set_index('DateTime', inplace=True)

    del df['Date']
    del df['Ticker']
    del df['Time']
    del df['Per']

    df['RSI_14'] = ta.RSI(df["Close"],timeperiod=14)
    df['RSI_10'] = ta.RSI(df["Close"],timeperiod=10)
    df['RSI_6'] = ta.RSI(df["Close"],timeperiod=6)
    df['RSI_2'] = ta.RSI(df["Close"],timeperiod=2)
    df['MOM_8'] = ta.MOM(df["Close"], timeperiod=8)
    df['MOM_4'] = ta.MOM(df["Close"], timeperiod=4)
    df['ATR_14'] = ta.ATR(df["High"], df["Low"], df["Close"], timeperiod=14)
    df['ATR_10'] = ta.ATR(df["High"], df["Low"], df["Close"], timeperiod=10)
    df['ATR_6'] = ta.ATR(df["High"], df["Low"], df["Close"], timeperiod=6)
    df['VAR'] = ta.VAR(df["Close"], timeperiod=5, nbdev=1)

    df['MA_10'] = ta.MA(df["Close"], timeperiod=10, matype=0)
    df['MA_30'] = ta.MA(df["Close"], timeperiod=30, matype=0)
    df['MA_50'] = ta.MA(df["Close"], timeperiod=50, matype=0)
    df['MA_200'] = ta.MA(df["Close"], timeperiod=200, matype=0)

    df['MACD'],macdsignal, macdhist = ta.MACD(df["Close"], fastperiod=12, slowperiod=26, signalperiod=9)

    df = df.iloc[200:]

    return df
