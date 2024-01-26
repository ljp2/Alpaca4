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

while True:
    try:
        d = client.get_crypto_latest_bar(request_params=request)['BTC/USD']
        t,o,h,l,c = d.timestamp, d.open, d.high, d.low, d.close
        now = datetime.now().strftime("%H:%M:%S")
        s = f'{now}  {t.strftime("%H:%M:%S")}  {o:.2f}  {h:.2f}  {l:.2f}  {c:.2f}'
        with open('test-stream.txt', 'a') as file:
            file.write(s+'\n')
        sleep(60)
    except Exception as e:
        print(e)
        sleep(3)


    