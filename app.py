from flask import Flask
from flask import request
from flask import render_template
from flask import url_for,redirect,flash
from flask import session, escape
#import requests
#import twyth
import pythontwitter2
import storage

app = Flask(__name__)


app.debug=True





@app.route('/login', methods= ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('homepage.html')
    else:
        user = request.form['username']
        password = request.form['password']
        res = 0
	if user and password:
	    res = storage.validate(user, password)
	if res == 1:
	    return redirect(url_for("search"))
        else:
            return render_template('homepage.html', res = res)


@app.route('/index', methods= ['GET'])
def index():
    return render_template ('index.html')

        

     


@app.route('/register', methods= ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        uname = request.form['username']
        print uname
        password = request.form['pswd']
        print password
        fullname = request.form['name']
        print fullname
        tuname = request.form['twitter']
        print tuname
        result = storage.addUser(uname, password, fullname, tuname)
        print "Result" + str(result)
        if result == 1:
            return redirect(url_for("login"))

@app.route('/search')
def search():
    return render_template('search.html')

import os
key = os.urandom(24)
#print key
app.secret_key = key




if __name__ == '__main__':
    app.run()
