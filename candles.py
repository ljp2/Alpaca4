import pandas as pd
from datetime import datetime, timedelta

import alpaca.data.models as alpaca_models

def calculate_heiken_ashi(df):
    ha_df = pd.DataFrame(index=df.index, columns=['open', 'high', 'low', 'close'])
    for i in range(len(df)):
        if i == 0:
            ha_df.iloc[i] = df.iloc[i]
        else:
            ha_df.at[df.index[i], 'open'] = (ha_df.at[df.index[i-1], 'open'] + ha_df.at[df.index[i-1], 'close']) / 2
            ha_df.at[df.index[i], 'close'] = (df.at[df.index[i], 'open'] + df.at[df.index[i], 'high'] + df.at[df.index[i], 'low'] + df.at[df.index[i], 'close']) / 4
            ha_df.at[df.index[i], 'high'] = max(df.at[df.index[i], 'high'], ha_df.at[df.index[i], 'open'], ha_df.at[df.index[i], 'close'])
            ha_df.at[df.index[i], 'low'] = min(df.at[df.index[i], 'low'], ha_df.at[df.index[i], 'open'], ha_df.at[df.index[i], 'close'])
    return ha_df

class Bar:
    def __init__(self, timestamp:datetime, open:float, high:float, low:float, close:float):
        self.timestamp:datetime = timestamp
        self.open:float = open
        self.high:float = high
        self.low:float = low
        self.close:float = close

    def __str__(self):
        return f'{self.open:.2f} {self.high:.2f} {self.low:.2f} {self.close:.2f}'
    
class Bars:
    def __init__(self, df:pd.DataFrame):
        if df is None:
            self.last_timestamp = None
            self.df = pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close'])
        else:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df.set_index('timestamp', inplace=True)
            self.df = df[['open', 'high', 'low', 'close']].copy()
            self.last_timestamp = df.index[-1]
            
    def add(self, bar:alpaca_models.bars.Bar):
        if self.last_timestamp is None:
            self.last_timestamp = bar.timestamp
            self.df.loc[bar.timestamp] = [bar.open, bar.high, bar.low, bar.close]
        else:
            if bar.timestamp - self.last_timestamp > timedelta(minutes=1):
                self.df.loc[bar.timestamp, 'high'] = max(self.df.loc[bar.timestamp, 'high'], bar.high)
                self.df.loc[bar.timestamp, 'low'] = min(self.df.loc[bar.timestamp, 'low'], bar.low)
                self.df.loc[bar.timestamp, 'close'] = bar.close
            else:
                self.last_timestamp = bar.timestamp
        self.df.loc[bar.timestamp] = [bar.open, bar.high, bar.low, bar.close]
    
    