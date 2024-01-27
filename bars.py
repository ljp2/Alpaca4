import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import alpaca.data.models as alpaca_models
from math import sqrt
from alpaca_api import getHistoricalCryptoBars
import matplotlib.pyplot as plt

import numpy as np

def dema_last(series, period):
    # Convert the series to a pandas Series if it's not already
    series = pd.Series(series)
    # Calculate the first EMA
    ema1 = series.ewm(span=period, adjust=False).mean()
    # Calculate the second EMA
    ema2 = ema1.ewm(span=period, adjust=False).mean()
    # Calculate the DEMA
    dema = 2 * ema1 - ema2
    # Return the last value
    return dema.iloc[-1]

def simple_moving_average_last(values, period):
    if len(values) < period:
        return np.nan
    else:
        return sum(values[-period:]) / period
    
def weighted_moving_average_last(values, period):
    if len(values) < period:
        return None
    weights = list(range(1, period + 1))
    weighted_values = values[-period:]
    return sum(w*v for w, v in zip(weights, weighted_values)) / sum(weights)

def hull_moving_average_last(values, period):
    if len(values) < period:
        return np.nan
    def wma(values, n):
        return sum((n - i) * values[-(n - i)] for i in range(n)) / ((n * (n + 1)) / 2)
    wma_short = 2 * wma(values, int(period / 2))
    wma_long = wma(values, period)
    diff = wma_short - wma_long
    hma_period = int(sqrt(period))
    hma = wma(values, hma_period)
    hma += diff
    return hma

class HAbars(pd.DataFrame):
    @property
    def _constructor(self):
        return HAbars

    def __init__(self, df=None, *args, **kwargs):
        if df is None:
            df = pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close'])
        else:
            df = df.copy()
            for i in range(len(df)):
                if i == 0:
                    df.iloc[i] = df.iloc[i]
                else:
                    df.at[df.index[i], 'open'] = (df.at[df.index[i-1], 'open'] + df.at[df.index[i-1], 'close']) / 2
                    df.at[df.index[i], 'close'] = (df.at[df.index[i], 'open'] + df.at[df.index[i], 'high'] + df.at[df.index[i], 'low'] + df.at[df.index[i], 'close']) / 4
                    df.at[df.index[i], 'high'] = max(df.at[df.index[i], 'high'], df.at[df.index[i], 'open'], df.at[df.index[i], 'close'])
                    df.at[df.index[i], 'low'] = min(df.at[df.index[i], 'low'], df.at[df.index[i], 'open'], df.at[df.index[i], 'close'])
        super().__init__(df, *args, **kwargs)

    def add_bar(self, new_bar:pd.Series):
        ha_close = (new_bar['open'] + new_bar['high'] + new_bar['low'] + new_bar['close']) / 4
        if len(self.bars) == 0:
            ha_open = (new_bar['open'] + new_bar['close']) / 2
        else:
            ha_open = (self.bars.iloc[-1]['open'] + self.bars.iloc[-1]['close']) / 2
        ha_high = max(new_bar['high'], ha_open, ha_close)
        ha_low = min(new_bar['low'], ha_open, ha_close)
        self.bars = self.bars.append({'timestamp': new_bar['timestamp'], 'open': ha_open, 'high': ha_high, 'low': ha_low, 'close': ha_close}, ignore_index=True)

class Bars(pd.DataFrame):
    _tohlc_cols = ['timestamp', 'open', 'high', 'low', 'close']
    _ohlc_cols = ['open', 'high', 'low', 'close']
    _ma_cols = ['maopen', 'mahigh', 'malow', 'maclose']
    _all_cols = _tohlc_cols + _ma_cols
    
    def __init__(self):
        data = pd.DataFrame(columns=self._all_cols)
        super().__init__(data)

    def add_row(self, tohlc, periods):
        row = {attr:getattr(tohlc, attr) for attr in self._tohlc_cols}
        for i,key in enumerate(self._ohlc_cols):
            period = periods[key]
            values = self[key].values
            if len(values) < period:
                row[self._ma_cols[i]] = np.nan
            else:
                row[self._ma_cols[i]] = hull_moving_average_last(self[key].values, period)
        self.loc[len(self)] = row

symbol = "BTC/USD"
end = datetime.now()
start = end - timedelta(hours=4)
bars = getHistoricalCryptoBars(symbol, start, end)
b = Bars()

for x in bars:
    st = x.timestamp.strftime('%H:%M:%S')
    sohlc = f'{x.open:.2f} {x.high:.2f} {x.low:.2f} {x.close:.2f}'
    # print(f'{st} {sohlc}')
    b.add_row(x, {'open': 9, 'high': 5, 'low': 5, 'close': 9})


# b[['maopen', 'mahigh', 'malow', 'maclose']].plot()
b[['mahigh', 'malow']].plot()
plt.show()
    