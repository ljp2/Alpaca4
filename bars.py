import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import alpaca.data.models as alpaca_models
from math import sqrt
from alpaca_api import getHistoricalCryptoBars
import matplotlib.pyplot as plt

import params

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



def bars_process(queues):

    symbol = "BTC/USD"
    _tohlc_cols = ['timestamp', 'open', 'high', 'low', 'close']
    _ohlc_cols = ['open', 'high', 'low', 'close']
    _ma_cols = ['maopen', 'mahigh', 'malow', 'maclose']
    _all_cols = _tohlc_cols + _ma_cols
    periods = {'open': 9, 'high': 5, 'low': 9, 'close': 5}

    bars = pd.DataFrame(columns=_all_cols)

    def add_row_bars(data_bar):
        row = {attr:getattr(data_bar, attr) for attr in _tohlc_cols}
        for i,key in enumerate(_ohlc_cols):
            period = periods[key]
            values = bars[key].values
            if len(values) < period:
                row[_ma_cols[i]] = np.nan
            else:
                row[_ma_cols[i]] = hull_moving_average_last(values, period)
        bars.loc[len(bars)] = row

    def init_bars():
        end = datetime.now()
        start = end - timedelta(hours=1)
        data = getHistoricalCryptoBars(symbol, start, end)
        for x in data:
            add_row_bars(x)


    init_bars()
    queues['init_bars'].put(bars)

    
if __name__ == '__main__':
    bars_process(None)


    # for x in bars:
    #     st = x.timestamp.strftime('%H:%M:%S')
    #     sohlc = f'{x.open:.2f} {x.high:.2f} {x.low:.2f} {x.close:.2f}'
    #     # print(f'{st} {sohlc}')
    #     b.add_bar(x, {'open': 9, 'high': 5, 'low': 5, 'close': 9})


    # b[['maopen', 'mahigh', 'malow', 'maclose']].plot()
    # b.bars[['mahigh', 'malow']].plot()
    # plt.show()
        