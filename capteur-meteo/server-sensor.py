#!flask/bin/python
from flask import Flask
import urllib2
import bme280

app = Flask(__name__)

@app.route('/')
def index():
    return bme280.get_temperature()

if __name__ == '__main__':
    app.run(host='10.0.1.230', port=5000, debug=True)


