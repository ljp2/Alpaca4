import pandas as pd
from datetime import datetime, timedelta
from alpaca_api import getHistoricalCryptoBars

from bars import Bars

class BarsN():
    _tohlc_cols = ['timestamp', 'open', 'high', 'low', 'close']
    _ohlc_cols = ['open', 'high', 'low', 'close']
    
    def __init__(self, grouping_N:int=5):
        self.grouping_N = grouping_N
        self.bars_n = []
        for i in range(self.grouping_N):
            self.bars_n.append(pd.DataFrame(columns=self._tohlc_cols))
        
    def add_row(self, df:pd.DataFrame):
        if len(df) < self.grouping_N:
            return
        subdf = df.iloc[-self.grouping_N:].copy()
        index = subdf.index[0]
        t = subdf.timestamp.iloc[0]
        o = subdf.open.iloc[0]
        c = subdf.close.iloc[-1]
        h = subdf.high.max()
        l = subdf.low.min()
        row = [t,o,h,l,c]
        n = len(df) % self.grouping_N     
        tf = self.bars_n[n]
        tf.loc[index] = row
        
if __name__ == '__main__':
    symbol = "BTC/USD"
    end = datetime.now()
    start = end - timedelta(hours=4)
    bars = getHistoricalCryptoBars(symbol, start, end)
    
    b = Bars()
    bn = BarsN()
    
    for x in bars:
        b.add_row(x, {'open': 9, 'high': 5, 'low': 5, 'close': 9})
        bn.add_row(b)
        
    pass

