import multiprocessing
import pandas as pd
from datetime import datetime, timedelta
from time import sleep

from alpaca.data.historical.crypto import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoLatestBarRequest

from keys import paper_apikey, paper_secretkey
ALPACA_API_KEY = paper_apikey
ALPACA_SECRET_KEY = paper_secretkey

client = CryptoHistoricalDataClient(ALPACA_API_KEY, ALPACA_SECRET_KEY)
request=CryptoLatestBarRequest(symbol_or_symbols='BTC/USD')

def get_bars_process(queues):
    bars_queue:multiprocessing.Queue = queues["bars"]
    info_queue:multiprocessing.Queue = queues["info"]
    client = CryptoHistoricalDataClient(ALPACA_API_KEY, ALPACA_SECRET_KEY)
    request=CryptoLatestBarRequest(symbol_or_symbols='BTC/USD')
    while True:
        try:
            d = client.get_crypto_latest_bar(request_params=request)['BTC/USD']
            print(type(d))
            bar = (d.timestamp, d.open, d.high, d.low, d.close)
            bars_queue.put(bar)
            info_queue.put(bar)
            sleep(60)
        except Exception as e:
            print(e)
            sleep(3)
    