#!flask/bin/python
from flask import Flask
import urllib2

app = Flask(__name__)

@app.route('/')
def status():
    result = ""
    try:
    	result += urllib2.urlopen("http://10.0.1.230:5000/").read()
    except urllib2.URLError:
	result += "{error:'error'}"
    result += "</br>"
    try:
    	result += urllib2.urlopen("http://10.0.1.231:5000/").read()
    except urllib2.URLError:
	result += "{error:'error'}"
    return result

if __name__ == '__main__':
    app.run(host='192.168.150.30', port=80, debug=True)


