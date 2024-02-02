import yfinance as yf
import pandas as pd


def fetch_stock_hist(stock,period="10mo"):
    # Fetch data for a specific stock, e.g., OMX30 index
    data = yf.Ticker(stock)

    # Get historical data for this stock
    hist = data.history(period=period)

    # Process the historical data
    hist.reset_index(inplace=True)
    hist['Date'] = pd.to_datetime(hist['Date']).dt.date
    hist = hist[['Date', 'Close']]
    return hist

