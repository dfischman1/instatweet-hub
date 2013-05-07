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
res = 0
app = Flask(__name__)


app.debug=True

CONFIG = {
    'client_id': '2e1ab1ca522343a589a4dc84eb31af41',
    'client_secret': '67b832ed8a9b4e67b8696a3db0a69fd2',
    'redirect_uri': 'http://ml7.stuycs.org:6379/instagram'
}

user_id = 0
user_token= 0
instagram_client = client.InstagramAPI(**CONFIG)
global user_hashtag
global uname
global success
success = ""
def process_tag_update(update):
    print update

@app.route('/')
def default():
    return redirect( url_for( 'login'))

storage.continuousUpdate()

@app.route('/login', methods= ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('homepage.html', success = success)
    else:
        global uname
        global password
        uname = request.form['username']
        password = request.form['password']
        res = 0
        if uname and password:
            res = storage.validate(uname, password)
        if res == 1:
            return redirect(url_for("search", uname=uname))
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
        if btn == "Submit":
            global success
            global user_hashtag
            global uname
            uerror = ""
            uname = ""
            password = ""
            fullname = ""
            
            user_hashtag = ""
            uname = request.form['username']
            password = request.form['pswd']
            fullname = request.form['name']
            user_hashtag = request.form['hashtag']
            tunames = []
            x = request.form['tuname']
           
            if x != "":
                
                 tunames.append(x)

            x = request.form['tuname2']
           
            if x != "":
                
                 tunames.append(x)

            x = request.form['tuname3']
           
            if x != "":
                 tunames.append(x)
        
            #print "hello" + tunames[0] + tunames[1] + tunames[2]
                
            
            

        
            for x in range(0, len(tunames)):
                if pythontwitter2.tweets.check(tunames[x]) != 1:
                    uerror = "Some of your twitter info isn't valid. Try again."
                    result = 0
                    return render_template('register.html', uerror = uerror)
            if storage.validate(uname, password) == 3:
                if password != "" and fullname != "" and user_hashtag != "" and uname != "" and len(tunames) != 0:
                    result = storage.addUser(uname, password, fullname, tunames, user_hashtag)
                    print storage.addTweets(uname)
                    success = ""
                    print "Your user info:"
                    print storage.getInfo(uname)
                    print storage.getTweets(uname)
                    success = "You succesfully created a new account!"
                    print success
                    #VALUES = {
                     #   'uname': uname,
                      #  'user_hashtag': user_hashtag,
                       #          }
                    return redirect(url_for('instaregister', uname=uname, user_hashtag=user_hashtag))
                #render_template('register.html', terror
            else:
                print "hello" +  tunames[0]
                uerror = "Some of your user info is invalid. Please try again."
                return render_template('register.html', uerror = uerror)
                #if result == 1:
                #    success = "You succesfully created a new account!"
                #   return redirect(url_for("login"))
                #if result == 0:


@app.route('/instaregister', methods = ['GET', 'POST'])
def instaregister():
    global api
    if request.method == 'GET':
        uname = request.args.get('uname')
        return render_template('instaregister.html', res = res, uname=uname)
    else:
        btn = request.form['Go']
    if btn == "Instagram":
        print request.args.keys()
        uname = request.args.get('uname')
        #user_hashtag=request.args.get('user_hashtag')
        queries='?' + 'uname='+uname
        api = client.InstagramAPI(client_id='2e1ab1ca522343a589a4dc84eb31af41',
                                  client_secret='67b832ed8a9b4e67b8696a3db0a69fd2',
                                  redirect_uri='http://ml7.stuycs.org:6379/instagram' + queries)
        return redirect(api.get_authorize_url(scope=['basic']))
    else:
        return redirect(url_for('login'))

#CONFIG = {
#    'client_id': '2e1ab1ca522343a589a4dc84eb31af41',
#    'client_secret': '67b832ed8a9b4e67b8696a3db0a69fd2',
#    'redirect_uri': 'http://ml7.stuycs.org:6376/instagram'
#}

#user_id = 0
#user_token= 0
#instagram_client = client.InstagramAPI(**CONFIG)


@app.route('/search')
def search():
    uname = request.args.get('uname')
    storage.addTweets(uname)
    if request.method == 'GET':
        try:
            storage.getInstaInfo(uname)
            pics = instagramhub.user_pics(uname)
            tweets = storage.getTweets(uname)
            print storage.getTweets(uname)
            return render_template("instagram.html", tweets = tweets, images = pics, user_hashtag = user_hashtag)
        except:
            tweets = storage.getTweets(uname)
            print "Here are your tweets" + tweets
            return render_template("instagram.html", tweets = tweets,user_hashtag = user_hashtag)
@app.route('/instagram')
def instagram():
    print 'start'
    #global uname
    #global user_hashtag
    uname = request.args.get('uname')
    user_hashtag = storage.getHash(uname)
    print request.args.keys()
    print uname
    print user_hashtag
    print request.args.get('code')
    try:
        code = request.args.get('code')
    except:
        res = "Missing Code, Please try again"
        return redirect(url_for('instaregister', res = res, uname=uname))
    try:
        print '1'
        code = request.args.get('code')
        print code
        print api
        access_token, instagram_user = api.exchange_code_for_access_token(code)
        print '2'
        print access_token
    except:
        res = "No token, please try again"
        return redirect(url_for('instaregister', res = res))
    user_id = instagram_user['id']
    user_token = access_token
    result = storage.addInstagram(uname, user_token, user_id)
    print user_id + user_hashtag + result
    taggedimages = instagramhub.get_pics(user_id, user_token, user_hashtag)
    print "Your username" + uname
    print storage.getInfo(uname)
    storage.addTweets(uname)
    tweets = storage.getTweets(uname)
    print tweets
    #print "Here are your tweets" + tweets
    print taggedimages
    return render_template('instagram.html', tweets = tweets, images = taggedimages, user_hashtag = user_hashtag)


import os
key = os.urandom(24)
#print key
app.secret_key = key




if __name__ == '__main__':
    app.run()
