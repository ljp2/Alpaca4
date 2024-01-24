import pandas as pd

def calculate_heiken_ashi(df):
    ha_df = pd.DataFrame(index=df.index, columns=['Open', 'High', 'Low', 'Close'])

    for i in range(len(df)):
        if i == 0:
            ha_df.iloc[i] = df.iloc[i]
        else:
            ha_df.at[df.index[i], 'Open'] = (ha_df.at[df.index[i-1], 'Open'] + ha_df.at[df.index[i-1], 'Close']) / 2
            ha_df.at[df.index[i], 'Close'] = (df.at[df.index[i], 'Open'] + df.at[df.index[i], 'High'] + df.at[df.index[i], 'Low'] + df.at[df.index[i], 'Close']) / 4
            ha_df.at[df.index[i], 'High'] = max(df.at[df.index[i], 'High'], ha_df.at[df.index[i], 'Open'], ha_df.at[df.index[i], 'Close'])
            ha_df.at[df.index[i], 'Low'] = min(df.at[df.index[i], 'Low'], ha_df.at[df.index[i], 'Open'], ha_df.at[df.index[i], 'Close'])

    return ha_df

# Example usage
df = pd.DataFrame({'Open': [10, 20, 30, 40],
                   'High': [15, 25, 35, 45],
                   'Low': [5, 15, 25, 35],
                   'Close': [12, 22, 32, 42]})

heiken_ashi_df = calculate_heiken_ashi(df)
print(heiken_ashi_df)
