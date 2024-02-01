import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from time import sleep
from math import sqrt

import alpaca.data.models as alpaca_models
from alpaca_api import getHistoricalCryptoBars
from alpaca.data.historical.crypto import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoLatestBarRequest

from moving_averages import weighted_moving_average_last

from keys import paper_apikey, paper_secretkey
ALPACA_API_KEY = paper_apikey
ALPACA_SECRET_KEY = paper_secretkey

import matplotlib.pyplot as plt



def bars_process(queues):
    symbol = "BTC/USD"
    _tohlc_cols = ['timestamp', 'open', 'high', 'low', 'close']
    _ohlc_cols = ['open', 'high', 'low', 'close']
    _ma_cols = ['maopen', 'mahigh', 'malow', 'maclose']
    _all_cols = _tohlc_cols + _ma_cols
    periods = {'open': 9, 'high': 5, 'low': 9, 'close': 5}
    client = CryptoHistoricalDataClient(ALPACA_API_KEY, ALPACA_SECRET_KEY)
    request=CryptoLatestBarRequest(symbol_or_symbols='BTC/USD')

    bars = pd.DataFrame(columns=_all_cols)

    def add_row_to_bars(data_bar):
        row = {attr:getattr(data_bar, attr) for attr in _tohlc_cols}
        row['timestamp'] = row['timestamp'].timestamp()
        for i,key in enumerate(_ohlc_cols):
            period = periods[key]
            values = bars[key].values
            if len(values) < period:
                row[_ma_cols[i]] = np.nan
            else:
                row[_ma_cols[i]] = weighted_moving_average_last(values, period)
        bars.loc[len(bars)] = row

    def init_bars():
        end = datetime.utcnow()
        start = end - timedelta(hours=1)
        data = getHistoricalCryptoBars(symbol, start, end)
        for x in data:
            add_row_to_bars(x)


    init_bars()
    # queues['init_bars'].put(bars)
    print(bars.tail(2))
    
    last_timestamp = bars.iloc[-1].timestamp
    
    i = 1
    while True:
        try:
            print(f't{i}', end=' ', flush=True)
            i += 1
            bar = client.get_crypto_latest_bar(request_params=request)['BTC/USD']
            if bar.timestamp.timestamp() == last_timestamp:
                sleep(5)
                continue
            else:
                print()
                i = 1
                print('adding bar', bar)
                add_row_to_bars(bar)
                last_timestamp = bar.timestamp.timestamp()
                print(bars.tail(2))
                # sleep(50)
                sleep(5)
        except Exception as e:
            print(e)
            sleep(3)
    

if __name__ == '__main__':
    bars_process(None)
