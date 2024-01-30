
from datetime import datetime, timedelta
from multiprocessing import Process, Queue
from time import sleep

from alpaca_api import getHistoricalCryptoBars
from alpaca.data.historical.crypto import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoLatestBarRequest

from keys import paper_apikey, paper_secretkey
ALPACA_API_KEY = paper_apikey
ALPACA_SECRET_KEY = paper_secretkey

import params
from bars import Bars
from barsN import BarsN

def initialize_trading(symbol):
    bars = Bars()
    bars_n = BarsN()
    end = datetime.now()
    start = end - timedelta(hours=1)
    for b in getHistoricalCryptoBars(symbol, start, end):
        bars.add_bar(b)
        bars_n.add_row(bars.bars)
    return bars, bars_n


def main(symbol):
    queues = {
        "bars": Queue(),
        "plot": Queue(),
        "info": Queue(),    
    }
    bars, bars_n = initialize_trading(symbol)
    
    print(bars.bars)
    for i in range(5):
        print(bars_n.bars_n[i])
        
    last_n = bars.bars.index[-1]
    
    pass

if __name__ == '__main__':
    main('BTC/USD')