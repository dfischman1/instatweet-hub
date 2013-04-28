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
    'redirect_uri': 'http://localhost:5000/search'
}

user_id = 0
user_token= 0
instagram_client = client.InstagramAPI(**CONFIG)
user_hashtag = 'potato'

def process_tag_update(update):
    print update


@app.route('/', methods= ['GET', 'POST'])
def default():
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
    elif request.form['Go'] == 'twitter':
        uname = request.form['username']
        password = request.form['pswd']
        fullname = request.form['name']
        tuname = request.form['twitter']
        user_hashtag = request.form['hashtag']
        storage.addUser(uname, password, fullname, tuname)
        return render_template('register.html', message = "now login with instagram")
    else:
        return redirect(instagram_client.get_authorize_url(scope=['basic']))

        

@app.route('/search')
def search():
    if request.method == 'GET':
        return render_template('search.html')

@app.route('/instagram')
def instagram():
    code = request.values.get('code')
    if not code:
        res = "Missing Code"
        return render_template('homepage.html', res = res)
    #try:
    access_token, instagram_user = instagram_client.exchange_code_for_access_token(code)
    if not access_token:
        res = "no token"
        return render_template('homepage.html', res = res)
    user_id = instagram_user['id']
    user_token = access_token
    print user_id + 'YAY!'
    images = instagramhub.get_pics(user_id, user_token)
    return render_template('instagram.html', images = images)
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
