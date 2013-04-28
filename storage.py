from pymongo import Connection


connection = Connection('mongo2.stuycs.org')
db=connection.admin
db.authenticate('ml7','ml7')
db = connection.roundtable
db.roundtable.save({})
db.roundtable.insert({'username':'Teehan', 'password':'devyldogs','full':'Daniel Teehan'})
clct=db.roundtable

def addUser(uname, password, fullname, tuname):
    if len(list(clct.find({'username':uname})))==0:
        clct.insert({'username':uname, 'password':password, 'full': fullname, 'tuname':tuname})
        return 1
    else:
        print "username is already taken, try another"
        return 0

def validate(uname, password):
    if len(list(clct.find({'username':uname})))==1:
        if len(list(clct.find({'username':uname,'password': password})))==1:
            return 1
        else:
            return 2
    else:
        return "no such account exists, create a new account"

def changePass(uname, oldpass, newpass):
    if len(list(clct.find({'username':uname,'password': oldpass})))==1:
        clct.update({'username':uname,'password':oldpass},{'username':uname,'password':newpass})

def reset():
    clct.drop()

reset()
addUser('Daniel','dobby','Daniel Teehan', 'teeman')
#print validate('Daniel', 'dobby')

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
