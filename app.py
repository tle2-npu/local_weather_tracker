# Import the Flask class
from flask import Flask

# Create an instance of the Flask class
app = Flask(__name__)

# Define a route with the @app.route decorator
@app.route('/')
def home():  
    "default route"
    return '<h1>Hello, World! From my first Flask app!</h1>'


@app.route('/about')
def about():
    return 'This is the About page.'

if __name__ == '__main__':
    app.run(debug=True)