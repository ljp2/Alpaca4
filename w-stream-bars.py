from alpaca.data.live import CryptoDataStream
import alpaca.data.models as models

from keys import paper_apikey, paper_secretkey
apikey = paper_apikey
secretkey = paper_secretkey

crypto_stream = CryptoDataStream(apikey, secretkey)

def write_bar_data(bar:models.Bar, filename):
    z = f"{bar.timestamp},{bar.open},{bar.high},{bar.low},{bar.close},{bar.volume}\n"
    with open(filename, 'a') as file:
        file.write(z)

# usage
# write_bar_data(bar, 'output.txt')
    
    
# async handler
async def bar_data_handler(bar:models.Bar):
    # quote data will arrive here
    z = f"{bar.timestamp},{bar.open},{bar.high},{bar.low},{bar.close},{bar.volume}\n"
    with open('test-stream.txt', 'a') as file:
        file.write(z)
    print('bar', z)

async def updated_bar_data_handler(bar:models.Bar):
    # quote data will arrive here
    z = f"{bar.timestamp},{bar.open},{bar.high},{bar.low},{bar.close},{bar.volume}\n"
    with open('test-stream.txt', 'a') as file:
        file.write(z)
    print('upd', z)

crypto_stream.subscribe_bars(bar_data_handler, "BTC/USD")
crypto_stream.subscribe_updated_bars(updated_bar_data_handler, "BTC/USD")

crypto_stream.run()
