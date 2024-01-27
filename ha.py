import pandas as pd

class HAbars(pd.DataFrame):
    def __init__(self, df=None, *args, **kwargs):
        if df is None:
            df = pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close'])
        else:
            df = df.copy()
            for i in range(len(df)):
                if i == 0:
                    df.iloc[i] = df.iloc[i]
                else:
                    df.at[df.index[i], 'open'] = (df.at[df.index[i-1], 'open'] + df.at[df.index[i-1], 'close']) / 2
                    df.at[df.index[i], 'close'] = (df.at[df.index[i], 'open'] + df.at[df.index[i], 'high'] + df.at[df.index[i], 'low'] + df.at[df.index[i], 'close']) / 4
                    df.at[df.index[i], 'high'] = max(df.at[df.index[i], 'high'], df.at[df.index[i], 'open'], df.at[df.index[i], 'close'])
                    df.at[df.index[i], 'low'] = min(df.at[df.index[i], 'low'], df.at[df.index[i], 'open'], df.at[df.index[i], 'close'])
        super().__init__(df, *args, **kwargs)

    def add_bar(self, new_bar:pd.Series):
        ha_close = (new_bar['open'] + new_bar['high'] + new_bar['low'] + new_bar['close']) / 4
        if len(self.bars) == 0:
            ha_open = (new_bar['open'] + new_bar['close']) / 2
        else:
            ha_open = (self.bars.iloc[-1]['open'] + self.bars.iloc[-1]['close']) / 2
        ha_high = max(new_bar['high'], ha_open, ha_close)
        ha_low = min(new_bar['low'], ha_open, ha_close)
        self.bars = self.bars.append({'timestamp': new_bar['timestamp'], 'open': ha_open, 'high': ha_high, 'low': ha_low, 'close': ha_close}, ignore_index=True)
