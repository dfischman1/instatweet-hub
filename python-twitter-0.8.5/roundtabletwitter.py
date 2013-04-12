import twitter

consumer_key = 'LvMwTBueTS3IsN7sLIoaIA'
consumer_secret = '	0cdq8IZwccRMBPrwH9odVoCUaeLSH4RSx9df4'

access_token = '295398619-lSehg93ixJJ80M4DyOtwpSsmnFzP70Ld4bpRInXm'
access_token_secret = 'BttSbnwFY14Ysa68d5Xxcy3ZKi8eUgevNLgxq9Xo'

api = twitter.Api(consumer_key = consumer_key, consumer_secret = consumer_secret,
                  access_token_key = access_token, access_token_secret = access_token_secret)

#proof of concept
def getTweets(username):
    i = 0
    statuses = api.GetUserTimeline(username)
    text = [s.text for s in statuses]
    while i < 4:
        print text[i] + "\n"
        i += 1
    



getTweets("@mets")