from alpaca.data.live import CryptoDataStream
import alpaca.data.models as models
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoLatestQuoteRequest
from datetime import datetime
from time import sleep

import pytz
eastern = pytz.timezone('US/Eastern')

from keys import paper_apikey, paper_secretkey
apikey = paper_apikey
secretkey = paper_secretkey

crypto_stream = CryptoDataStream(apikey, secretkey)
hist_client = CryptoHistoricalDataClient(apikey, secretkey)

# def get_latest_bar():
#     params = CryptoLatestQuoteRequest(symbol_or_symbols='BTC/USD')
#     bar = hist_client.get_crypto_latest_bar(request_params=params)['BTC/USD']
#     return bar

def write_bar_data(bar:models.Bar, s:str):
    z = f"{bar.timestamp.astimezone(eastern)},{bar.open},{bar.high},{bar.low},{bar.close},{bar.volume}\n"
    with open('test-stream.txt', 'a') as file:
        file.write(z)

def print_bar(bar:models.Bar, s:str):
    z = f"{s} {bar.timestamp.astimezone(eastern)},{bar.open},{bar.high},{bar.low},{bar.close},{bar.volume}\n"
    print(z)

async def bar_data_handler(bar:models.Bar):
    write_bar_data(bar, 'bar')
    print_bar(bar, 'bar')

try:
    crypto_stream.subscribe_bars(bar_data_handler, "BTC/USD")
    crypto_stream.run()
except KeyboardInterrupt:
    exit(0)
except Exception as e:
        print(f'Exception from websocket connection: {e}')
finally:
    print("Trying to re-establish connection")
    sleep(3)
    crypto_stream.subscribe_bars(bar_data_handler, "BTC/USD")
    crypto_stream.run()
