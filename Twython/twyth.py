
from twython import Twython

oauth_token = ""
oauth_token_secret = ""
def get_url():
    app_key = 'LvMwTBueTS3IsN7sLIoaIA'
    app_secret = '0cdq8IZwccRMBPrwH9odVoCUaeLSH4RSx9df4'
    
    access_token = '295398619-lSehg93ixJJ80M4DyOtwpSsmnFzP70Ld4bpRInXm'
    access_token_secret = 'BttSbnwFY14Ysa68d5Xxcy3ZKi8eUgevNLgxq9Xo'
    t = Twython(app_key=app_key,
                app_secret=app_secret,
                callback_url='http://127.0.0.1:5000/register')
    
    auth_props = t.get_authentication_tokens()
    oauth_token = auth_props['oauth_token']
    print "Oauth_token:" + oauth_token
    oauth_token_secret = auth_props['oauth_token_secret']
    #a = auth_props['oauth_verifier']
      
    print 'Connect to Twitter via: %s' % auth_props['auth_url']
    auth_url =  auth_props['auth_url']
    
    t = Twython(app_key=app_key,
            app_secret=app_secret,
            oauth_token=oauth_token,
            oauth_token_secret=oauth_token_secret)
    
#user_timeline = t.getUserTimeline(screen_name='nytimes')
    return auth_url
    
   

get_url()

