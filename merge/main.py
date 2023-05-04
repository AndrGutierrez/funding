import pandas as pd

# Read the funding CSV file into a DataFrame
funding_file='funding_binance'
funding_df = pd.read_csv(f'{funding_file}.csv')

# Read the candles CSV file into a DataFrame
candles_df = pd.read_csv('BTC-USD-4h-2022-05-01T04:00.csv')

# Merge the two DataFrames based on the datetime column in candles_df and Time column in funding_df
merged_df = pd.merge(candles_df, funding_df, left_on='datetime', right_on='Time', how='left')
merged_df = merged_df.drop('Time', axis=1)
# Print the merged DataFrame
print(merged_df)
merged_df.to_csv(f'merged_{funding_file}.csv',index=False)
