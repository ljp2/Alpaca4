import pandas as pd
from datetime import datetime
from time import sleep

from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoLatestQuoteRequest

from keys import paper_apikey, paper_secretkey
apikey = paper_apikey
secretkey = paper_secretkey

client = CryptoHistoricalDataClient(apikey, secretkey)

params = CryptoLatestQuoteRequest(symbol_or_symbols='BTC/USD')

q = client.get_crypto_latest_bar(request_params=params)['BTC/USD']

z = "{}  {}\t{:0.2f}   {:0.2f}   {:0.2f}   {:0.2f}".format(
    datetime.utcnow().strftime('%H:%M:%S'),
    q.timestamp.strftime('%H:%M:%S'),  q.open, q.high, q.low, q.close)     
print(z)
        