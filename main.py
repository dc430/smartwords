from flask import Flask, render_template, flash, session, request, abort, redirect
from flask_bootstrap import Bootstrap
import os
import json
import pandas as pd
import random
app = Flask(__name__)

Bootstrap(app)   

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
    return render_template('listone.html', result = [df, temp, random])

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)



