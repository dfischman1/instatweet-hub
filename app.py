from flask import Flask
from flask import request
from flask import render_template
from flask import url_for,redirect,flash
from flask import session, escape
#import requests
#import twyth
#import tweets
import storage
db = storage.db()

app = Flask(__name__)


app.debug=True





@app.route('/', methods= ['GET', 'POST'])
def default():
    if request.method == 'GET':
        return render_template('homepage.html')
    else:
        button = request.form["Go"]
        if button == "register":
            return redirect( url_for("register"))
        else:
            results = 2
            user = request.form['username']
            password = request.form['password']
            results = db.validate(user, password)
            if results == True:
                return redirect(url_for('http://www.nytimes.com'))
            else:
                return render_template('homepage.html', results = results)




@app.route('/register', methods= ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        success = db.adduser(request.form['username'], request.form['pswd'], request.form['name'], request.form['twitterhandle'])
        if success != None:
            return redirect(url_for('http://www.nytimes.com'))
        else:
            return render_template('register.html', success = success)
        
            

        

     



import os
key = os.urandom(24)
#print key
app.secret_key = key




if __name__ == '__main__':
    app.run()
