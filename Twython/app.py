from flask import Flask
from flask import request
from flask import render_template
from flask import url_for,redirect,flash
from flask import session, escape
import requests
import twyth

app = Flask(__name__)


app.debug=True







@app.route('/')
def default():
     return render_template('index.html')

     


@app.route('/register')
def register():
     auth_url = twyth.get_url()
     #twyth.callback()
     return render_template('register.html', auth_url = auth_url)


import os
key = os.urandom(24)
#print key
app.secret_key = key




if __name__ == '__main__':
    app.run()
