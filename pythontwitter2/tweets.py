import twitter


def get_tweets(username):
    tweets = []
    i = 0
    api = twitter.Api()
    app_key = 'LvMwTBueTS3IsN7sLIoaIA'
    app_secret = '0cdq8IZwccRMBPrwH9odVoCUaeLSH4RSx9df4'
    access_token = '295398619-lSehg93ixJJ80M4DyOtwpSsmnFzP70Ld4bpRInXm'
    access_token_secret = 'BttSbnwFY14Ysa68d5Xxcy3ZKi8eUgevNLgxq9Xo'
    
    api = twitter.Api(consumer_key='consumer_key',
                      consumer_secret='consumer_secret',
                      access_token_key='access_token',
                      access_token_secret='access_token_secret')
    
    statuses = api.GetUserTimeline(username)
    text = [s.text for s in statuses]
    while i < 10:
        tweets.append(text[i])
        #print tweets[i] + "\n"
        i += 1
    return tweets


def get_hashtag(tweets, hashtag):
    matches = []
    y = 1
    for word in tweets:
        #print "" + str(y) + " " + word + "/n"
        for i in word.split():
            if i == hashtag:
                #print "" + str(y) + " " + word + "/n"
                y += 1
                matches.append(word)
    return matches




def get_easy(username, hashtag):
    matches = get_hashtag(get_tweets(username), hashtag)
    return matches


def check(username):
    try:
        get_tweets(username)
        print "success!"
        return 1
    except:
        print "twitter username doesn't exist"
        return 0

#get_easy('mets', '#Mets')




