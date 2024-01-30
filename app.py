from flask import Flask, render_template,jsonify
from omxindex import omx_hist

app = Flask(__name__)
@app.route('/data')
def data():
    return jsonify(omx_hist.to_dict(orient='records'))

@app.route('/')
def index():
    greeting = "Hello"
    return render_template('index.html', greeting=greeting)

if __name__ == '__main__':
    app.run(debug=True)
