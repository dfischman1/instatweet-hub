from flask import Flask
from flask import request
from flask import render_template
from flask import url_for,redirect,flash
from flask import session, escape
#import requests
#import twyth
import tweets
import storage

app = Flask(__name__)


app.debug=True





@app.route('/', methods= ['GET', 'POST'])
def default():
    if request.method == 'GET':
        return render_template('homepage.html')
    else:
        user = request.form['username']
        password = request.form['password']
        results = storage.validate(self, user, password)
        if results:
            return redirect(url_for('index'))
        else:
            return render_template('homepage.html', results = results)


@app.route('/index', methods= ['GET'])
def index():
    return render_template ('index.html')

        

     


@app.route('/register')
def register():
    return render_template('register.html')


import os
key = os.urandom(24)
#print key
app.secret_key = key




if __name__ == '__main__':
    app.run()
