from alpaca.data.live import CryptoDataStream

from keys import paper_apikey, paper_secretkey
apikey = paper_apikey
secretkey = paper_secretkey

crypto_stream = CryptoDataStream(apikey, secretkey)

# async handler
async def bar_data_handler(data):
    # quote data will arrive here
    print("\nbar data")
    print(data)

async def updated_bar_data_handler(data):
    # quote data will arrive here
    print("\nUpdated bar data")
    print(data)

crypto_stream.subscribe_bars(bar_data_handler, "BTC/USD")
crypto_stream.subscribe_updated_bars(updated_bar_data_handler, "BTC/USD")

crypto_stream.run()
