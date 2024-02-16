import yfinance as yf
import pandas as pd

# fetch data for omx with 10 months as default period
def fetch_omx_hist(period="10mo"):
    # Fetch data 
    omx30 = yf.Ticker("^OMX")

    
    hist = omx30.history(period=period)

  
    hist.reset_index(inplace=True)
    hist['Date'] = pd.to_datetime(hist['Date']).dt.date
    hist = hist[['Date', 'Close']]
    return hist


