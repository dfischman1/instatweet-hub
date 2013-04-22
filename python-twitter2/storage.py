from pymongo import Connection

class db:
    def __init__(self,db="roundtable"):
        self.connection = Connection('mongo2.stuycs.org')
        self.db=self.connection.admin
        self.db.authenticate('ml7','ml7')
        self.db = self.connection.roundtable
        self.db.roundtable.save({})
        self.db.roundtable.insert({'username':'Teehan', 'password':'devyldogs','full':'Daniel Teehan'})

    def addUser(self, uname, password, fullname):
        clct = self.db.roundtable
        if len(list(clct.find({'username':uname})))==0:
            clct.insert({'username':uname, 'password':password, 'full': fullname})
        else:
            print "username is already taken, try another"

    def validate(self, uname, password):
        clct = self.db.roundtable
        if len(list(clct.find({'username':uname})))==1:
            if len(list(clct.find({'username':uname,'password': password})))==1:
                return True
            else:
                return "wrong password, try again"
        else:
            return "no such account exists, create a new account"

    def changePass(self, uname, oldpass, newpass):
        clct = self.db.roundtable
        if len(list(clct.find({'username':uname,'password': oldpass})))==1:
            clct.update({'username':uname,'password':oldpass},{'username':uname,'password':newpass})

    def reset(self):
        self.db.roundtable.drop()


if __name__=="__main__":
    db  = db()
    db.addUser("daniel teehan", 'daelin', 'daelin fisch')
    db.addUser("Leopold","specswag", "leo spon")
    db.addUser("Patrick", "cadabra", " P Soup")
    db.addUser("Daelin","Nightlin", "Night Lin")
    db.addUser("Daelin","Nightlin", "Night")  #should not be allowed
    print db.validate("Daelin","Nightlin")    #should be true
    db.changePass('Daelin','Nightlin','Daylin')
    print db.validate("Daelin", "Daylin")  #should be true, as pass has been changed
    print db.validate("Daelin", "Nightlin") #should be false, as pass has been changed
    db.reset()
