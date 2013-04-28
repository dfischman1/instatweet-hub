from flask import Flask
from flask import request
from flask import render_template
from flask import url_for,redirect,flash
from flask import session, escape
#import requests
import pythontwitter2.tweets
import storage

app = Flask(__name__)


app.debug=True

pythontwitter2.tweets.get_easy('nytimes', 'a')



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
            return render_template('homepage.html', res = res, success = "")


@app.route('/index', methods= ['GET'])
def index():
    return render_template ('index.html')

        

     


@app.route('/register', methods= ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        terror = ""
        uerror = ""
        uname = request.form['username']
        print uname
        password = request.form['pswd']
        print password
        fullname = request.form['name']
        print fullname
        tuname = request.form['twitter']
        print tuname
        if pythontwitter2.tweets.check(tuname) == 1:
            if storage.validate(uname, password) == 3:
                result = storage.addUser(uname, password, fullname, tuname)
            else:
                uerror = "That username isn't valid. Try again"
                result = 0

        else:
            terror = "Your twitter username isn't valid. Try again."
            result = 0
        if result == 1:
            success = "You succesfully created a new account!"
            return redirect(url_for("login"))
        if result == 0:
            return render_template('register.html',
                                   terror = terror,
                                   uerror = uerror)
    

@app.route('/search')
def search():
    return render_template('search.html')

import os
key = os.urandom(24)
#print key
app.secret_key = key




if __name__ == '__main__':
    app.run()
