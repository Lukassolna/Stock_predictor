import yfinance as yf
import pandas as pd


# Fetch data for a specific stock, e.g., OMX30 index
omx30 = yf.Ticker("^OMX")

# Get historical data for this stock
hist = omx30.history(period="10mo")

# Display the first few rows of the data
hist.reset_index(inplace=True)
hist['Date'] = pd.to_datetime(hist['Date']).dt.date
hist= hist[['Date','Close']]
omx_hist=hist
