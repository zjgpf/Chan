import pandas as pd
from Utility import getStock

ticker = '601229.ss'
def findTop(ticker):
    df = getStock(ticker)
    df_yesterday = df.shift(1)
    df_tomorrow = df.shift(-1)
    df['c1'] = df['High']>df_yesterday['High']
    df['c2'] = df['Low']>df_yesterday['Low']
    df['c3'] = df['High']>df_tomorrow['High']
    df['c4'] = df['Low']>df_tomorrow['Low']
    df['Top'] = df.apply(lambda row: row.c1 and row.c2 and row.c3 and row.c4, axis = 1)
    return df.index[df['Top']].tolist()

# contain relation
def findTopBottomCR(ticker):
    df = getStock(ticker)
    length = df.shape[0]

    #u_High: up trend high
    df['u_High'] = 0.0
    df['u_Low'] = 0.0
    df['d_High'] = 0.0
    df['d_Low'] = 0.0
    df['trend'] = 0
    df.set_value(df.index[0], 'u_High', df.iloc[0].High)
    df.set_value(df.index[0], 'u_Low',  df.iloc[0].Low)
    df.set_value(df.index[0], 'trend',  1)
    topDate = []
    bottomDate = []
    for i in range(1, length):
        # up trend Take the higher value for both High and Low
        if df.iloc[i].High > df.iloc[i-1].u_High and df.iloc[i].Low > df.iloc[i-1].u_Low and df.iloc[i-1].trend == 1:
            df.set_value(df.index[i], 'u_High', df.iloc[i].High)
            df.set_value(df.index[i], 'u_Low', df.iloc[i].Low)
            df.set_value(df.index[i], 'trend', 1)
            
        elif df.iloc[i].High >= df.iloc[i-1].u_High and df.iloc[i].Low <= df.iloc[i-1].u_Low and df.iloc[i-1].trend == 1:
            df.set_value(df.index[i], 'u_High', df.iloc[i].High)
            df.set_value(df.index[i], 'u_Low', df.iloc[i-1].u_Low)
            df.set_value(df.index[i], 'trend', 1)
            
        elif df.iloc[i].High <= df.iloc[i-1].u_High and df.iloc[i].Low >= df.iloc[i-1].u_Low and df.iloc[i-1].trend == 1:
            df.set_value(df.index[i], 'u_High', df.iloc[i-1].u_High)
            df.set_value(df.index[i], 'u_Low', df.iloc[i].Low)
            df.set_value(df.index[i], 'trend', 1)
            
        #Top shape confirmed
        elif df.iloc[i].High < df.iloc[i-1].u_High and df.iloc[i].Low < df.iloc[i-1].u_Low and df.iloc[i-1].trend == 1:
            df.set_value(df.index[i], 'd_High', df.iloc[i].High)
            df.set_value(df.index[i], 'd_Low', df.iloc[i].Low)
            df.set_value(df.index[i], 'trend', -1)
            topDate.append(df.index[i])
            
        # up trend Take the lower value for both High and Low 
        elif df.iloc[i].High < df.iloc[i-1].d_High and df.iloc[i].Low < df.iloc[i-1].d_Low and df.iloc[i-1].trend == -1:
            df.set_value(df.index[i], 'd_High', df.iloc[i].High)
            df.set_value(df.index[i], 'd_Low', df.iloc[i].Low)
            df.set_value(df.index[i], 'trend', -1)

        elif df.iloc[i].High <= df.iloc[i-1].d_High and df.iloc[i].Low >= df.iloc[i-1].d_Low and df.iloc[i-1].trend == -1:
            df.set_value(df.index[i], 'd_High', df.iloc[i].High)
            df.set_value(df.index[i], 'd_Low', df.iloc[i-1].d_Low)
            df.set_value(df.index[i], 'trend', -1)

        elif df.iloc[i].High >= df.iloc[i-1].d_High and df.iloc[i].Low <= df.iloc[i-1].d_Low and df.iloc[i-1].trend == -1:
            df.set_value(df.index[i], 'd_High', df.iloc[i-1].d_High)
            df.set_value(df.index[i], 'd_Low', df.iloc[i].Low)
            df.set_value(df.index[i], 'trend', -1)

        #Bottom shape confirmed
        elif df.iloc[i].High > df.iloc[i-1].d_High and df.iloc[i].Low > df.iloc[i-1].d_Low and df.iloc[i-1].trend == -1:
            df.set_value(df.index[i], 'u_High', df.iloc[i].High)
            df.set_value(df.index[i], 'u_Low', df.iloc[i].Low)
            df.set_value(df.index[i], 'trend', 1)
            bottomDate.append(df.index[i])

    return [df, topDate, bottomDate]
 
[df, topDate, bottomDate] = findTopBottomCR(ticker)
l1 = findTop(ticker)
print(len(l1))
print(len(topDate))
