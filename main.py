from sql_connection.pw import password
from sql_connection.sql import seb
import numpy as np
df_seb=(seb(password))

# 4 parameters (Change, RSI,percentage_diff,10_change) to predict next_day change

def verify(dataframes):
    if not dataframes:
        raise ValueError("No DataFrames provided.")
    reference_dates = dataframes[0]['date']

    for i, df in enumerate(dataframes[1:], start=1):
        if not df['date'].equals(reference_dates):
            raise ValueError(f"The 'date' column in DataFrame {i} does not match the reference 'date' column.")
def change_percentage(df):
    df['Change'] = (df['Change'] / (df['close'] - df['Change'])) * 100
    return df

def change_column(df):
    # Create 'next_day_change' column by shifting 'Change' up by one
    df['next_day_change'] = df['Change'].shift(-1)
    # Fill the last row's 'next_day_change' with 0
    df['next_day_change']=df['next_day_change'].fillna(0)
    return df

def add_sma_10(df, column_name):
    # Calculate the 10-day Simple Moving Average (SMA) for the specified column
    sma_column_name = f'SMA_10_{column_name}'
    df[sma_column_name] = df[column_name].rolling(window=10, min_periods=1).mean()
    return df

def add_percentage_diff(df, price_column, sma_column):
    # differnece between sma and price
    df['percentage_diff'] = (df[price_column].astype(float) / df[sma_column].astype(float) -1) 
    return df

def add_10_day_change(df, change_column):
    # Ensure the 'Change' column is numeric
    df[change_column] = df[change_column].astype(float)

    # Calculate the 10-day sum of changes
    df['temp']=df[change_column] /100 +1
    df['10_change'] =  df['temp'].rolling(window=10, min_periods=1).apply(np.prod, raw=True)-1
    df.drop(columns='temp',inplace=True)
    
    return df

# Apply the function to your DataFrame

df_seb = add_sma_10(df_seb, 'close')
df_seb = add_percentage_diff(df_seb, 'close', 'SMA_10_close')
df_seb = change_percentage(df_seb)
df_seb = change_column(df_seb)
df_seb = add_10_day_change(df_seb, 'Change')
print(df_seb)
correlation = df_seb['RSI'].corr(df_seb['Change'])
print(correlation)