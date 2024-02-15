from sql_connection.pw import password
from sql_connection.sql import sql_to_pandas
import numpy as np
from new_stock_attempt import fetch_all

df_seb=(sql_to_pandas("seb",password))
df_sbb=(sql_to_pandas("sbb",password))
df_hexa=sql_to_pandas("hexa",password)
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
    # Create 'next_day_change' column
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
    df['percentage_diff'] = (df[price_column].astype(float) / df[sma_column].astype(float) -1)*100 
    return df

def add_10_day_change(df, change_column):
    # Ensure the 'Change' column is numeric
    df[change_column] = df[change_column].astype(float)
    # Calculate the 10-day sum of changes
    df['temp']=df[change_column] /100 +1
    df['10_change'] = (df['temp'].rolling(window=10, min_periods=1).apply(np.prod, raw=True) - 1) * 100
    df.drop(columns='temp',inplace=True)
    
    return df

def create_columns(df):
    df = add_sma_10(df, 'close')
    df = add_percentage_diff(df, 'close', 'SMA_10_close')
    df= change_percentage(df)
    df = change_column(df)
    df= add_10_day_change(df, 'Change')
    return df




df_seb=create_columns(df_seb)
df_sbb=(create_columns(df_sbb))
df_hexa=create_columns(df_hexa)

dfs= [df_seb,df_sbb,df_hexa]