import yfinance as yf
import pandas as pd


def fetch_omx_hist(period="10mo"):
    # Fetch data for a specific stock, e.g., OMX30 index
    omx30 = yf.Ticker("^OMX")

    # Get historical data for this stock
    hist = omx30.history(period=period)

    # Process the historical data
    hist.reset_index(inplace=True)
    hist['Date'] = pd.to_datetime(hist['Date']).dt.date
    hist = hist[['Date', 'Close']]
    return hist

# Now you can call fetch_omx_hist with a specific period when needed
omx_hist = fetch_omx_hist("10mo")