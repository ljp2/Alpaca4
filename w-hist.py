
import pandas as pd

from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta

from keys import paper_apikey, paper_secretkey
apikey = paper_apikey
secretkey = paper_secretkey

client = CryptoHistoricalDataClient(apikey, secretkey)

end = datetime.utcnow()
start = end - timedelta(hours=1)

request_params = CryptoBarsRequest(
                        symbol_or_symbols=["BTC/USD"],
                        timeframe=TimeFrame.Minute,
                        start=start,
                        end=end
                 )

data = client.get_crypto_bars(request_params=request_params)

bars = data["BTC/USD"]  
for b in bars:
       print(b)
