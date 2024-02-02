import yfinance as yf
import pandas as pd


def fetch_stock_hist(stock,period="10mo"):
    # Fetch data 
    data = yf.Ticker(stock)
    hist = data.history(period=period)
    hist.reset_index(inplace=True)
    hist['Date'] = pd.to_datetime(hist['Date']).dt.date
    hist = hist[['Date', 'Close']]
    return hist

