from flask import Flask, render_template, jsonify, request
from omxindex import fetch_omx_hist
import yfinance as yf
import datetime
from new_stock_attempt import fetch_all
from global_var import omx
app = Flask(__name__)

@app.route('/data')
def data():
    inputPeriod = request.args.get('period', default='10mo')  # Get 'period' from query params or default to '10mo'
    omx_hist = fetch_omx_hist(period=inputPeriod)
    return jsonify(omx_hist.to_dict(orient='records'))

@app.route('/daily')
def daily():
    dataframes = fetch_all()  # Fetch the array of dataframes
    last_rows = []
    for i, df in enumerate(dataframes):
        last_row = df.iloc[-1].to_dict()  # Extract the last row as a dictionary
        last_row['name'] = omx[i]  # Add the corresponding name from the omx array
        last_rows.append(last_row)
    return jsonify(last_rows)  # Return the list of dictionaries as JSON
@app.route('/')
def index():
    greeting = "Hello"
    return render_template('index.html', greeting=greeting)

@app.route('/stock/<stock_name>')
def stock_detail(stock_name):
    # You can fetch additional data about the stock here if needed
    return render_template('stock_detail.html', stock_name=stock_name)




if __name__ == '__main__':
    app.run(debug=True)


