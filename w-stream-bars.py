from alpaca.data.live import CryptoDataStream
from alpaca.data.historical import CryptoHistoricalDataClient

import alpaca.data.models as models
from pytz import timezone
import pytz

from keys import paper_apikey, paper_secretkey
apikey = paper_apikey
secretkey = paper_secretkey

crypto_stream = CryptoDataStream(apikey, secretkey)

def write_bar_data(bar:models.Bar, filename):
    z = f"{bar.timestamp.astimezone(timezone('US/Eastern'))},{bar.open},{bar.high},{bar.low},{bar.close},{bar.volume}\n"
    with open(filename, 'a') as file:
        file.write(z)

def print_bar_data(bar:models.Bar):
    z = f"{bar.timestamp.astimezone(timezone('US/Eastern'))},{bar.open},{bar.high},{bar.low},{bar.close},{bar.volume}\n"
    print(z)

def get_latest_crypto_bar(symbol: str, bar_minutes: int):
    client = CryptoHistoricalDataClient(apikey, secretkey)
    latest_quote = client.get_crypto_latest_quote('BTC/USD')
    return latest_quote
    
# async handler
async def bar_data_handler(bar:models.Bar):
    write_bar_data(bar, 'test-stream.txt')
    print_bar_data(bar)

async def updated_bar_data_handler(bar:models.Bar):
    write_bar_data(bar, 'test-stream-upd.txt')
    print_bar_data(bar)


crypto_stream.subscribe_bars(bar_data_handler, "BTC/USD")
crypto_stream.subscribe_updated_bars(updated_bar_data_handler, "BTC/USD")

crypto_stream.run()
