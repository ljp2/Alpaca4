from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoLatestQuoteRequest

from keys import paper_apikey, paper_secretkey
apikey = paper_apikey
secretkey = paper_secretkey

client = CryptoHistoricalDataClient(apikey, secretkey)

params = CryptoLatestQuoteRequest(symbol_or_symbols='BTC/USD')

q = client.get_crypto_latest_quote(request_params=params)['BTC/USD']

print(f"{q.timestamp.strftime('%H:%M:%S')}\t{q.ask_price:.2f}")