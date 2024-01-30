from flask import Flask, render_template, jsonify, request
from omxindex import fetch_omx_hist
import yfinance as yf

app = Flask(__name__)

@app.route('/data')
def data():
    inputPeriod = request.args.get('period', default='10mo')  # Get 'period' from query params or default to '10mo'
    omx_hist = fetch_omx_hist(period=inputPeriod)
    return jsonify(omx_hist.to_dict(orient='records'))

@app.route('/')
def index():
    greeting = "Hello"
    return render_template('index.html', greeting=greeting)

if __name__ == '__main__':
    app.run(debug=True)
