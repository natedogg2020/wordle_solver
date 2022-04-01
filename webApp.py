#!/usr/bin/python3

'''
setup instructions:
in bash:

export FLASK_APP=webApp
export FLASK_ENV=development
flask run

'''
from array import array
from json import JSONEncoder
from flask import Flask, request
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def myapp():
    message = "To use this app: %s/add?x=value&y=value" % request.base_url
    return message
@app.route('/add')
def add():
    # Checking that both parameters have been supplied
    for param in ['x', 'y']:
        if not param in request.args:
            result = { 
                'type': '%s value is missing' % param, 
                'content': '', 
                'status': 'REQUEST_DENIED'
            }
            return jsonify(result)
    
    # Make sure they are numbers too
    # try:
    x = float(request.args['x'])
    # y = float(request.args['y'])
    y = str( request.args['y'])
    a = y.split(',')
    b = []
    for st in a:
        b.append(int(st))

    # except:
    #     return "x and y should be numbers"
    
    result = { 
        'type': 'result', 
        'content':  len( b), 
        'content2':  b, 
        'status': 'REQUEST_OK'
    }   
    return jsonify(result)