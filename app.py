from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Simple string to display
    greeting = "Hello"
    # Render the HTML template with the greeting
    return render_template('index.html', greeting=greeting)

if __name__ == '__main__':
    app.run(debug=True)
