#!/usr/bin/python3

'''
Setting up windows venv for VSCode
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

    # Print any repeat words, since repeats will break the search
    for i in range(len(lines)-1):
        if(lines[i] == lines[i + 1]):
            print("Warning, repeat word: ", lines[i])

    min_wc = 100000
    chosen_word = ""
    # Selected Remaining Matches dictionary
    srmat = {}
    all_it = ["aesir"]

#   Input SOARE into dictionary
    # for SOARE, so 1 loop (should remove)
    for w1 in all_it:
        #Remove whitespaces
        w1 = w1.strip()
        mat = {}
        rmat = {}
        # For every word in word list
        for w2 in lines:
            #Remove whitespaces
            w2 = w2.strip()
            # Calculate an array of 0/1/2 to look for possible words
            msum = calc_response_vector(w1,w2)
            # add or append w2 into rmat (remaining matches) dictionary 
            # so that once we get feedback, we can narrow down the list 
            # of words to check.
            if tuple(msum) not in rmat:
                rmat[tuple(msum)] = [w2]
            else:
                rmat[tuple(msum)].append(w2)
            mat[tuple([w1,w2])] = msum

        # check for which of remaining values is the best choice
        M = max([len(val) for val in rmat.values()])
        # New best choice, so update values
        if M < min_wc:
            min_wc = M  #Set new best choice val
            chosen_word = w1  # choose this current word
            srmat = rmat  # Narrow down remaining values

    round = 1


from functools import lru_cache

'''
    calc_response_vector is used to predetermine the remaining matches possible
    through creating an array called msum, which is essentially a replication
    of wordle's logic to decide if a letter in a word is yellow, green, or gray
    in respect to the target word.
    w2 is the target word, while w1 is to be checked against w2.
'''
@lru_cache(maxsize=None)
def calc_response_vector(w1,w2):
    tw2 = w2    # Temp word
    msum = [0 for i in range(5)]    # [0, 0, 0, 0, 0]
    # Check if w1 and w2 have exactly the same letter placement
    for c_ind in range(5):
        # Same letter, so put a 2 to signify a green
        if w1[c_ind] == tw2[c_ind]:
            msum[c_ind] = 2
            # Now replace this letter with a * so it isn't counted twice
            tw2 = tw2[:c_ind] + "*" + tw2[c_ind+1:]
    # Now check for any yellows
    for c_ind in range(5):
        # The temp word2 contains w1 letter and it's not already green, so set it to yellow
        if w1[c_ind] in tw2 and msum[c_ind] == 0:
            msum[c_ind] = 1
            # Now replace this letter with a * so it isn't counted twice
            ind_app = tw2.find(w1[c_ind]) # Finding index the yellow occurs to remove it from tempW2
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
            all_it = ["soare"]

        # Get Grey,Yellow, Green from webpage input
        x = float(request.args['x'])
        y = str( request.args['y'])
        a = y.split(',')
        b = []
        for st in a:
            b.append(int(st))

        print(chosen_word)

        feedback = tuple([int(el) for el in y.split(',')])
        # Narrow down possible remaining matches using the given feedback
        lines = srmat[feedback]
        # Check if there is only 1 guess left, and send it back if it is
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

        #For every word in word list
        for w1 in all_it:
            #Strip to make sure it's 5 letter words, no whitespace
            w1 = w1.strip()
            # initialize dictionaries
            mat = {}
            rmat = {}
            # For every word in possible remaining words
            for w2 in lines:
                #Strip to make sure it's 5 letter words, no whitespace
                w2 = w2.strip()
                # Calculate an array of 0/1/2 to look for possible words
                msum = calc_response_vector(w1,w2)
                # Check if rmat has an entry for the gray/yellow/green 
                # sequence for the current w1 and w2, and add or append 
                # it to the word list.
                if tuple(msum) not in rmat:
                    rmat[tuple(msum)] = [w2]
                else:
                    rmat[tuple(msum)].append(w2)
                mat[tuple([w1,w2])] = msum

            # check for which of remaining values is the best choice
            M = max([len(val) for val in rmat.values()])
            # New best choice, so update values
            if M < min_wc:
                min_wc = M #Set new best choice val
                chosen_word = w1 # choose this current word
                srmat = rmat # Narrow down remaining values
            
        result = { 
            'type': 'result', 
            'newGuess':  chosen_word, 
            'content2':  b, # array acknowledging letter matches
            'status': 'REQUEST_OK'
        }   
        round = round +1    # Increment round
        return jsonify(result)
    else:
        return jsonify(result = { 
            'type': 'result', 
            'newGuess':  chosen_word, 
            'content2':  '', 
            'status': 'REQUEST_OK'
        }  )






