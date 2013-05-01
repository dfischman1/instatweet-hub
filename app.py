from flask import Flask
from flask import request
from flask import render_template
from flask import url_for,redirect,flash
from flask import session, escape
from instagram import client, subscriptions
#import requests
#import twyth
import pythontwitter2
import storage
import instagramhub

app = Flask(__name__)


app.debug=True

CONFIG = {
    'client_id': '2e1ab1ca522343a589a4dc84eb31af41',
    'client_secret': '67b832ed8a9b4e67b8696a3db0a69fd2',
    'redirect_uri': 'http://localhost:5000/instagram'
}

user_id = 0
user_token= 0
instagram_client = client.InstagramAPI(**CONFIG)
user_hashtag = 'fun'
global success
success = ""
def process_tag_update(update):
    print update

@app.route('/')
def default():
    return redirect( url_for( 'login'))



@app.route('/login', methods= ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('homepage.html', success = success)
    else:
        user = request.form['username']
        password = request.form['password']
        res = 0
	if user and password:
	    res = storage.validate(user, password)
	if res == 1:
	    return redirect(url_for("search"))
        else:
            return render_template('homepage.html', res = "retry or register")


@app.route('/index', methods= ['GET'])
def index():
    return render_template ('index.html')

        

     


@app.route('/register', methods= ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        btn = request.form['Go']
	if btn == "Twitter":
            terror = ""
            uerror = ""
            uname = request.form['username']
            password = request.form['pswd']
            fullname = request.form['name']
            tunames = []
            for x in range(0,5):
                try:
                    tunames.append(request.form[str(x)])
                except:
                    break               
            user_hashtag = request.form['hashtag']
            for x in range(0, len(tunames)):
                if pythontwitter2.tweets.check(tunames[x]) != 1:
                    break
            
                global terror
                terror = "Your twitter username isn't valid. Try again."
                result = 0
                return render_template('register.html', terror = terror, uerror = uerror)
            else:
                if storage.validate(uname, password) == 3:
                    result = storage.addUser(uname, password, fullname, tunames, "")
                    global success
                    success = "You succesfully created a new account!"
                    return redirect(url_for('instaregister'))
                    #render_template('register.html', terror
                else:
                    uerror = "That username isn't valid. Try again"
                    result = 0
                    return render_template('register.html', terror = terorr,
                                           uerror = uerror)
            #if result == 1:
            #    success = "You succesfully created a new account!"
            #   return redirect(url_for("login"))
            #if result == 0:
                return render_template('register.html',
                                       terror = terror,
                                       uerror = uerror)
        

@app.route('/instaregister', methods = ['GET', 'POST'])
def instaregister():
    if request.method == 'GET':
        return render_template('instaregister.html')
    else:
        btn = request.form['Go']
    if btn == "Instagram":
           return redirect(instagram_client.get_authorize_url(scope=['basic']))
    else:
           return redirect(url_for('login'))




@app.route('/search')
def search():
    if request.method == 'GET':
        return render_template('search.html')

@app.route('/instagram')
def instagram():
    try:
        code = request.values.get('code')
    except:
        res = "Missing Code"
        return render_template('homepage.html', res = res)
    try:
        code = request.values.get('code')
        access_token, instagram_user = instagram_client.exchange_code_for_access_token(code)
    except:
        res = "no token"
        return render_template('homepage.html', res = res)
    user_id = instagram_user['id']
    user_token = access_token
    print user_id + user_hashtag + 'YAY!'
    taggedimages = instagramhub.get_pics(user_id, user_token, user_hashtag)
    print taggedimages
    return render_template('instagram.html', images = taggedimages, user_hashtag = user_hashtag)
        #deferred.defer(fetch_instagram_for_user, g.user.get_id(), count=20, _queue='instagram')
    #except (RuntimeError, TypeError, NameError):
    #    print "poops"
    #    return render_template('search.html')
    #return render_template('search.html')

import os
key = os.urandom(24)
#print key
app.secret_key = key




if __name__ == '__main__':
    app.run()
