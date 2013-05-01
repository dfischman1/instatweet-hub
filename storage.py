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
        return clct.find({'username':uname})[0]['hashtag']
    else:
        return "invalid username"
        
def addInstagram(uname, token, instaid):
    if len(list(clct.find({'username':uname})))==1:
        clct.update({'username':uname},{'instatoken':token, "instaid":instaid})
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
    print clct.drop()


def addTweets(uname, hashtag):
    for post in clct.find({'username': uname}):
        tunames = post['tunames']
        for i in tunames:      
            matches = pythontwitter2.tweets.get_easy(i, hashtag)
            for x in matches:
                clct.update({ 'username' : uname }, {'$addToSet': { 'tweets': x} })
                
def updateTweets():
    for post in clct.find():
        uname = post['username']
        hashtag = post['hashtag']
        addTweets(uname,hashtag)


def continuousUpdate():
    updateTweets()
    s=threading.Timer(10000.0,continuousUpdate)
    s.start()


    
    
def getTweets(uname):
    tweets=[]
    x = 0
    for post in clct.find({'username': uname}):
        for tweet in post['tweets']:
            tweets.append(tweet)
            x += 1
    twts= "You have " + str(x) + " tweets: "
    for i in tweets:
        twts = twts + "\n" + i
    return twts
            
    

#reset()
#addUser('Daniel','dobby','Daniel Teehan', 'leopoldsg94')
addUser('Ryan','winky','Ryan Teehan', ['RyanTeehan','leopoldsg94'], '#csproject')
print validate('Ryan', 'winky')


addTweets('Ryan','#csproject')

#print getTweets('Daniel')
print getTweets('Ryan')

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
