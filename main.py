from flask import Flask, render_template, flash, session, request, abort, redirect
from flask_bootstrap import Bootstrap
import os
import json
import pandas as pd
import random
app = Flask(__name__)

Bootstrap(app)   

counter = 0
words_done = []
@app.route('/')

def index():
    return render_template('index.html')


@app.route('/register')

def register():
    return render_template('register.html')

@app.route('/validate', methods=['POST'])
def validate():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
        session['Already clicked'] = True
    else:
        flash('wrong password!')
    return home()

@app.route('/home')
def home():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        return render_template('wordtest.html')

@app.route('/destroysession')
def destroysession():
    session['loggin_in'] = False
    session['Already clicked'] = False
    return index()


#List one
@app.route('/listone')
def listone():
    df = pd.read_json('static/json/Word_list_one.json')
    df = df.transpose()
    temp = []
    global words_done
    global counter
    return render_template('listone.html', result = [df, temp, random, counter, words_done])

#Check if the word is right
@app.route('/auth', methods=['POST'])
def auth():
    result = request.form
    print(result)
    f = open('answers.txt', 'a')
    global words_done
    global counter
    counter += 1
    words_done.append(result['word'])
    f.write(result['answer']+':'+result['word']+"\n")
    return listone()

#Calculate the effeciency score
@app.route('/endtest', methods=['POST'])
def endtest():
    #result = request.form
    global words_done
    global counter 
    words_done = []
    counter = 0
    df = pd.read_json('static/json/Word_list_one.json')
    df = df.transpose()
    t_s = 0
    total = 0
    wrong_words = []
    with open('answers.txt', 'r') as f:
        for line in f:
            family, word = line.split(':')
            word = word.replace('\n', '')
            total += 1
            for i in range(1, 128):
                if(df.iloc[i]['Word'] == word):
                    f = df.iloc[i]['Family']
                    if(family == f):
                        t_s += 1
                    else:
                        wrong_words.append(df.iloc[i]['Word'])
    open('answers.txt', 'w').close()
    return render_template("score.html", result = (t_s, total, (t_s/total)*100,wrong_words))


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)



