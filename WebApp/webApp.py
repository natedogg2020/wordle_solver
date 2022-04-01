#!/usr/bin/python3

'''

$ py -3.9 -m venv .venv
$ /venv/Scripts/activate.bat
$ code .


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

@app.route('/reset')
def reset():
    initValues()
    message = "Reset all Values :)"
    return message

def initValues():
    global lines
    global all_lines
    global all_it
    global round
    global min_wc
    global chosen_word
    global srmat
    global foundSol

    f = open("NewWord.txt","r")
    all_w = open("NewWord.txt","r")

    lines = f.readlines()
    all_lines = all_w.readlines()
    foundSol = False

    for i in range(len(lines)-1):
        if(lines[i] == lines[i + 1]):
            print(lines[i])
    min_wc = 100000
    chosen_word = ""
    srmat = {}
    all_it = ["aesir"]

    for w1 in all_it:
        w1 = w1.strip()
        mat = {}
        rmat = {}
        for w2 in lines:
            w2 = w2.strip()
            msum = calc_response_vector(w1,w2)
            if tuple(msum) not in rmat:
                rmat[tuple(msum)] = [w2]
            else:
                rmat[tuple(msum)].append(w2)
            mat[tuple([w1,w2])] = msum

        M = max([len(val) for val in rmat.values()])
        if M < min_wc:
            min_wc = M
            chosen_word = w1
            srmat = rmat

    round = 1

# f = open("words.txt","r")
# all_w = open("words.txt","r")

# f = open("NewWord.txt","r")
# all_w = open("NewWord.txt","r")

# lines = f.readlines()
# all_lines = all_w.readlines()



from functools import lru_cache

@lru_cache(maxsize=None)
def calc_response_vector(w1,w2):
    tw2 = w2
    msum = [0 for i in range(5)]
    for c_ind in range(5):
        if w1[c_ind] == tw2[c_ind]:
            msum[c_ind] = 2
            tw2 = tw2[:c_ind] + "*" + tw2[c_ind+1:]
    for c_ind in range(5):
        if w1[c_ind] in tw2 and msum[c_ind] == 0:
            msum[c_ind] = 1
            ind_app = tw2.find(w1[c_ind])
            tw2 = tw2[:ind_app] + "*" + tw2[ind_app+1:]
    return msum


initValues()

@app.route('/add')
def add():
    global lines
    global all_lines
    global all_it
    global round
    global min_wc
    global chosen_word
    global srmat
    global foundSol

    if(not foundSol):

        if round != 0:
            all_it = all_lines
        else:
            all_it = ["aesir"]

        
        
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
        
        print(chosen_word)
        # inp = input()
        # print(type(inp))
        print(type(a))
        print(type(b))
        feedback = tuple([int(el) for el in y.split(',')])
        lines = srmat[feedback]
        if len(lines) == 1:
            print("Done. Final word is {}".format(lines[0]))
            chosen_word = lines[0]
            print(chosen_word)
            result = { 
            'type': 'result', 
            'newGuess':  chosen_word, 
            'content2':  b, 
            'status': 'REQUEST_OK'
            }
            foundSol = True
            return jsonify(result)
            # exit(0)
        if(round > 5):
            print("Failed. Did not find word after 6 attempts")
        # Checking that both parameters have been supplied
        for param in ['x', 'y']:
            if not param in request.args:
                result = { 
                    'type': '%s value is missing' % param, 
                    'content': '', 
                    'status': 'REQUEST_DENIED'
                }
                return jsonify(result)

        # for round in range(6):


        for w1 in all_it:
            w1 = w1.strip()
            mat = {}
            rmat = {}
            for w2 in lines:
                w2 = w2.strip()
                msum = calc_response_vector(w1,w2)
                if tuple(msum) not in rmat:
                    rmat[tuple(msum)] = [w2]
                else:
                    rmat[tuple(msum)].append(w2)
                mat[tuple([w1,w2])] = msum

            M = max([len(val) for val in rmat.values()])
            if M < min_wc:
                min_wc = M
                chosen_word = w1
                srmat = rmat
            
        

        result = { 
            'type': 'result', 
            'newGuess':  chosen_word, 
            'content2':  b, 
            'status': 'REQUEST_OK'
        }   
        round = round +1
        return jsonify(result)
    else:
        return jsonify(result = { 
            'type': 'result', 
            'newGuess':  chosen_word, 
            'content2':  '', 
            'status': 'REQUEST_OK'
        }  )






