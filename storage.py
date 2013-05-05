from pymongo import Connection
import pythontwitter2.tweets
import threading

connection = Connection('mongo2.stuycs.org')
db=connection.admin
db.authenticate('ml7','ml7')
db = connection.roundtable
db.roundtable.save({})
db.roundtable.insert({'username':'Teehan', 'password':'devyldogs','full':'Daniel Teehan'})
clct=db.roundtable

def addUser(uname, password, fullname, tunames, hashtag):
    if len(list(clct.find({'username':uname})))==0:
        clct.insert({'username':uname, 'password':password, 'full': fullname, 'tunames':tunames, 
                    'tweets': [], 'imgs': [], 'hashtag':hashtag, 'instatoken':"", "instaid": ""})
        return 1
    else:
        print "username is already taken, try another"
        return 0
        
def getHash(uname):
    if len(list(clct.find({'username':uname})))==1:
        print clct.find({'username':uname})[0]['hashtag'][1:]
        return clct.find({'username':uname})[0]['hashtag'][1:]
    else:
        print clct.find({'username':uname})[0]['hashtag'][1:]
        return "invalid username"

def getTwitterHash(uname):
    if len(list(clct.find({'username':uname})))==1:
        print clct.find({'username':uname})[0]['hashtag']
        return clct.find({'username':uname})[0]['hashtag']
    else:
        print "NOOO"
        return "NOOO"
        
def getInfo(uname):
    info=[]
    if len(list(clct.find({'username':uname})))!=0:
        print clct.find({'username':uname})[0]
        print clct.find({'username':uname})[0]['username']
        print clct.find({'username':uname})[0]['password']
        print clct.find({'username':uname})[0]['full']
        print clct.find({'username':uname})[0]['tunames']
        print clct.find({'username':uname})[0]['hashtag']
    else:
        return "invalid username"
    return info
        
        
def addInstagram(uname, token, instaid):
    if len(list(clct.find({'username':uname})))==1:
        clct.update({'username':uname},{'$set': {'instaid':instaid}})
        clct.update({'username':uname},{'$set': {'instatoken':token}})
        print clct.find({'username':uname})[0].keys()
        return "Successful Update"
    else:   
        return "invalid username"
        
def validate(uname, password):
    if len(list(clct.find({'username':uname})))==1:
        if len(list(clct.find({'username':uname,'password': password})))==1:
            return 1
        else:
            return 2
    else:
        return 3
        return "no such account exists, create a new account"

def getInstaInfo(uname):
    ans = []
    ans.append(clct.find({'username':uname}))[0]['instaid']
    ans.append(clct.find({'username':uname}))[0]['instatoken']
    return ans

def changePass(uname, oldpass, newpass):
    if len(list(clct.find({'username':uname,'password': oldpass})))==1:
        clct.update({'username':uname,'password':oldpass},{'username':uname,'password':newpass})

def reset():
    for post in clct.find():
        print post
    print clct.drop()


def addTweets(uname):
    for post in clct.find({'username': uname}):
        tunames = post['tunames']
        hashtag = getTwitterHash(uname)
        print hashtag
        for i in tunames:      
            matches = pythontwitter2.tweets.get_easy(i, hashtag)
            for x in matches:
                clct.update({ 'username' : uname }, {'$addToSet': { 'tweets': x} })
        return clct.find({'username':uname})[0]['tweets']
                
def updateTweets():
    for post in clct.find():
        uname = post['username']
        addTweets(uname)


def continuousUpdate():
    updateTweets()
    s=threading.Timer(10000.0,continuousUpdate)
    s.start()


    
    
def getTweets(uname):
    tweets=[]
    x = 0
    for post in clct.find({'username': uname}):
        print post
        for tweet in post['tweets']:
            print tweet
            tweets.append(tweet)
            x += 1
    twts= "You have " + str(x) + " tweets: "
    for i in tweets:
        twts = twts + "\n" + i
    print twts
    return tweets
            
    


#reset()
#if validate('Daelin', 'winky') == 3:
#    addUser('Daelin','winky','Ryan Teehan', ['RyanTeehan'], '#csproject')#
#
#    print addTweets('Daelin')
#    success = ""
#    print "Your user info:"
#    getInfo('Daelin')
#    print getTweets('Daelin')
#    success = "You succesfully created a new account!"




#print validate('Daelin', 'winky')
#addTweets('Daelin')
#print getTweets('Daelin')

#if __name__=="__main__":
#    addUser("daniel teehan", 'daelin', 'daelin fisch', "@dfisch")
#    addUser("Leopold","specswag", "leo spon", "@leo")
#    addUser("Patrick", "cadabra", " P Soup", "@sarpshark")
#    addUser("Daelin","Nightlin", "Night Lin", "@nightlin")
#    addUser("Daelin","Nightlin", "Night", "@night")  #should not be allowed
#    print validate("Daelin","Nightlin")    #should be true
#    changePass('Daelin','Nightlin','Daylin')
#    print validate("Teehan", "devyldogs")
#    print validate("Daelin", "Daylin")  #should be true, as pass has been changed
#    print validate("Daelin", "Nightlin") #should be false, as pass has been changed
#    reset()
