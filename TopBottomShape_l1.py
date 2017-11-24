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
    df['isContain'] = False
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
            df.set_value(df.index[i], 'isContain', True)
            
        elif df.iloc[i].High <= df.iloc[i-1].u_High and df.iloc[i].Low >= df.iloc[i-1].u_Low and df.iloc[i-1].trend == 1:
            df.set_value(df.index[i], 'u_High', df.iloc[i-1].u_High)
            df.set_value(df.index[i], 'u_Low', df.iloc[i].Low)
            df.set_value(df.index[i], 'trend', 1)
            df.set_value(df.index[i], 'isContain', True)
            
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
            df.set_value(df.index[i], 'isContain', True)

        elif df.iloc[i].High >= df.iloc[i-1].d_High and df.iloc[i].Low <= df.iloc[i-1].d_Low and df.iloc[i-1].trend == -1:
            df.set_value(df.index[i], 'd_High', df.iloc[i-1].d_High)
            df.set_value(df.index[i], 'd_Low', df.iloc[i].Low)
            df.set_value(df.index[i], 'trend', -1)
            df.set_value(df.index[i], 'isContain', True)

        #Bottom shape confirmed
        elif df.iloc[i].High > df.iloc[i-1].d_High and df.iloc[i].Low > df.iloc[i-1].d_Low and df.iloc[i-1].trend == -1:
            df.set_value(df.index[i], 'u_High', df.iloc[i].High)
            df.set_value(df.index[i], 'u_Low', df.iloc[i].Low)
            df.set_value(df.index[i], 'trend', 1)
            bottomDate.append(df.index[i])

    return [df, topDate, bottomDate]

def resetTopBottomDate(df, topDate, bottomDate):
    top = []
    bottom = []
    for date in topDate:
        pEnd = df.index.get_loc(date)-1
        pStart = pEnd
        isContained = df.iloc[pStart].isContain
        while df.iloc[pStart].isContain:
            pStart = pStart-1
        if isContained:
            highest = df.iloc[pStart: pEnd+1].High.max()
            for i in range(pStart, pEnd+1):
                if df.iloc[i].High == highest:
                    top.append(df.index[i])
                    break
        else:
            top.append(df.index[pEnd])

    for date in bottomDate:
        pEnd = df.index.get_loc(date)-1
        pStart = pEnd
        isContained = df.iloc[pStart].isContain
        while df.iloc[pStart].isContain:
            pStart = pStart-1
        if isContained:
            lowest = df.iloc[pStart: pEnd+1].Low.min()
            for i in range(pStart, pEnd+1):
                if df.iloc[i].Low == lowest:
                    bottom.append(df.index[i])
                    break
        else:
            bottom.append(df.index[pEnd])
    return [top, bottom]

def drawLine(df, topDate, bottomDate):
    topDownList = []
    downTopList = []
    start = topDate[0]
    end = topDate[0]
    for date in topDate:
        if date < end:
            continue
        
        

    return downList

def findNextValidTopBottom(df, startDate, topBottomDate):
    p = df.index.get_loc(startDate)+1
    count = 0
    while count < 3:
        if df.iloc[p].isContain:
            p = p+1
            continue
        count = count+1
        p = p+1
    end = df.index[p]
    
    i = 0
    while topBottomDate[i] < end:
        i = i+1
    return topBottomDate[i]

##def findNextValidTop(df, startDate, topDate):
##    p = df.index.get_loc(startDate)+1
##    count = 0
##    while count < 3:
##        if df.iloc[p].isContain:
##            p = p+1
##            continue
##        count = count+1
##        p = p+1
##    end = df.index[p]
##    
##    i = 0
##    while topDate[i] < end:
##        i = i+1
##    return topDate[i]

def howManyStickBetweenTwoPeriod(df, start, end):
    df_s = df.ix[start]
    df_e = df.ix[end]
    count = 1
    p_start = df.index.get_loc(start)+1
    p_end = df.index.get_loc(end)
    while p_start <= p_end:
        if df.iloc[p_start].isContain:
            p_start = p_start+1
            continue
        else:
            p_start = p_start+1
            count = count+1
    return count
    

def test():
    [df, topDate, bottomDate] = findTopBottomCR(ticker)
    [top,bottom] = resetTopBottomDate(df, topDate, bottomDate)
    a = howManyStickBetweenTwoPeriod(df, top[1], bottom[1])
    print(a)


test()
##[df, topDate, bottomDate] = findTopBottomCR(ticker)
##downList = drawDown(df, topDate, bottomDate)
##print(downList)
