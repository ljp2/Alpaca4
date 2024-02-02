import sys
import numpy as np
import pandas as pd
from multiprocessing import Process, Queue

from moving_averages import weighted_moving_average_last
from bars import bars_process
    
symbol = "BTC/USD"
_tohlc_cols = ['timestamp', 'open', 'high', 'low', 'close']
_ohlc_cols = ['open', 'high', 'low', 'close']
_ma_cols = ['maopen', 'mahigh', 'malow', 'maclose']
_all_cols = _tohlc_cols + _ma_cols
periods = {'open': 9, 'high': 5, 'low': 9, 'close': 5}
grouping_N = 5

bars = pd.DataFrame(columns=_all_cols)
bars_n = []
for i in range(grouping_N):
    bars_n.append(pd.DataFrame(columns=_all_cols))

def add_row_to_bars(data_bar):
    row = {attr:getattr(data_bar, attr) for attr in _tohlc_cols}
    row['timestamp'] = row['timestamp'].timestamp()
    for i,key in enumerate(_ohlc_cols):
        period = periods[key]
        values = bars[key].values
        if len(values) < period:
            row[_ma_cols[i]] = np.nan
        else:
            row[_ma_cols[i]] = weighted_moving_average_last(values, period)
    bars.loc[len(bars)] = row
    
def update_barsN():
    if len(bars) < grouping_N:
        return
    subdf = bars.iloc[-grouping_N:].copy()
    index = subdf.index[0]
    t = subdf.timestamp.iloc[0]
    o = subdf.open.iloc[0]
    c = subdf.close.iloc[-1]
    h = subdf.high.max()
    l = subdf.low.min()
    mao =subdf.maopen.iloc[0]
    mac = subdf.maclose.iloc[-1]
    mah = subdf.mahigh.max()
    mal = subdf.malow.min()
    row = [t,o,h,l,c,mao,mah,mal,mac]
    n = len(bars) % grouping_N     
    tf = bars_n[n]
    tf.loc[index] = row


def main():
    queues = {
        "bars": Queue(),
        "plot": Queue(),
        "info": Queue(),    
    }

    try:
        get_bars_process = Process(target=bars_process, args=(queues,), daemon=True)
        get_bars_process.start()

        # wait for initial historical bars to initialize the bars dataframe
        res = queues['bars'].get()
        if res[0] == 'init':
            bars_init = res[1]
            for bar in bars_init:
                add_row_to_bars(bar)
                update_barsN()
        else:
            print('unknown resonse. should be init', res[0], flush=True)
            sys.exit(1)
          
        print()  
        print(bars.tail(), flush=True)
            
        # for i in range(grouping_N):
        #     print('bars_n', i)
        #     print(bars_n[i].tail())
        #     print()
            
        while True:
            res = queues['bars'].get()
            if res[0] == 'bar':
                bar = res[1]
                add_row_to_bars(bar)
                # update_barsN()
                print(bars.tail(), flush=True)
                print(flush=True)
                # for i in range(grouping_N):
                #     print('bars_n', i)
                #     print(bars_n[i].tail())
                #     print()
            else:
                print('unknown resonse. should be bar', res[0])
                sys.exit(1)

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully by terminating both processes
        get_bars_process.terminate()

if __name__ == "__main__":
    main()
    