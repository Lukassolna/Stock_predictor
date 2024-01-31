import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import os
import numpy as np
from global_var import omx
import pickle
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def fetch_stock_data(ticker):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=100*365)
    data = yf.download(ticker, start=start_date, end=end_date)
    if data.empty:
        raise Exception(f"No data available for ticker {ticker}")
    data = data[['Close']].reset_index()
    data['Change'] = data['Close'] / data['Close'].shift(1)
    data['Change'] = data['Change'].fillna(1)
    data['Change'] = data['Change']-1
    data['Delta'] = data['Close'].diff()
    data['Gain'] = data['Delta'].apply(lambda x: x if x > 0 else 0)
    data['Loss'] = data['Delta'].apply(lambda x: -x if x < 0 else 0)

    window_length = 14
    data['Avg_Gain'] = data['Gain'].rolling(window=window_length, min_periods=window_length).mean()
    data['Avg_Loss'] = data['Loss'].rolling(window=window_length, min_periods=window_length).mean()
    
    data['RS'] = data['Avg_Gain'] / data['Avg_Loss']
    
    data['RSI'] = 100 - (100 / (1 + data['RS']))
    # clean the data
    data.drop(columns='Delta',inplace=True)
    data.columns = ['date', 'close', 'Change', 'Up', 'Down', 'Av up', 'Av down', 'Relative', 'RSI']
    return data


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
    df.fillna(0, inplace=True)

    return df

def fetch_all(use_pickle=True, pickle_path='stock_data.pkl', max_age_hours=1):
    if use_pickle and os.path.exists(pickle_path):
        file_age_hours = (datetime.now() - datetime.fromtimestamp(os.path.getmtime(pickle_path))).total_seconds() / 3600
        if file_age_hours < max_age_hours:
            with open(pickle_path, 'rb') as file:
                return pickle.load(file)
    dfs=[]
    directory = 'new_csv_files' 
    for stock in omx:
        try:
            current = fetch_stock_data(stock)
            current=create_columns(current)
            dfs.append(current)
            current.to_csv(f'{directory}/{stock}.csv', index=False)

        except Exception as e:
            print(f"Error fetching data for {stock}: {e}")
    with open(pickle_path, 'wb') as file:
        pickle.dump(dfs, file)

    return dfs
dfs=fetch_all()


