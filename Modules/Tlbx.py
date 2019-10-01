import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, UserMixin


#Connectors to database
def dbConnect():
  db = pymysql.connect(host='ec2-3-16-158-152.us-east-2.compute.amazonaws.com', port=3306, user='Website', password='W3bsite!', db='PetConnect',autocommit=True)
  #db = pymysql.connect(host='127.0.0.1', port=3306, user='Website', password='W3bsite!', db='PetConnect',autocommit=True)
  cur = db.cursor()
  return cur
def dbConnectDict():
  db = pymysql.connect(host='ec2-3-16-158-152.us-east-2.compute.amazonaws.com', port=3306, user='Website', password='W3bsite!', db='PetConnect',autocommit=True)
  #db = pymysql.connect(host='127.0.0.1', port=3306, user='Website', password='W3bsite!', db='PetConnect',autocommit=True)
  cur = db.cursor(pymysql.cursors.DictCursor)
  return cur, db

#Validate that the Email does not already exist
def validate_email(email):
    cur= dbConnect()
    cur.execute("SELECT email from tUser WHERE email = '" + email+"';")
    Result = cur.fetchall()
    if Result is not ():   
        return False

#Insert the new account information into the database
def new_Account(firstName, lastName, email, password, address, city, state, zipCode):
    cur, db = dbConnectDict()
    addressQuery = ("INSERT INTO tAddress (address, city, state, zip) VALUES(%s, %s, %s, %s);")
    data = (address, city, state, zipCode)
    cur.execute(addressQuery, data)
    userQuery = ("INSERT INTO tUser (firstName, lastName, email, password, image, addressID) VALUES(%s, %s, %s, %s, %s, LAST_INSERT_ID());")
    image = None
    data = (firstName, lastName, email, password, image)
    cur.execute(userQuery, data)
    db.commit()
    

#Get the password from the database
def getPass(email):
    cur, db = dbConnectDict()
    cur.execute("SELECT password from tUser where email ='" + email +"';")
    password = cur.fetchone()
    
    #Causes crash if account does not exist
    password = password.get("password")
    return password

#Hash the password before committing to the database
def hash_password(password):
    password = generate_password_hash(password)
    return password

#Check that the hash and the password entered are the same.
def check_password(email, password):
    try:
        return check_password_hash(getPass(email), password)
    except: 
        return False

def loginUser(email):
    user = User(email)
    login_user(user)

class userRefresh(UserMixin):
    def __init__(self, id):
        cur, db = dbConnectDict()
        query = ("SELECT email, password from tUser where userID = '" + id + "';")
        cur.execute(query)
        user = cur.fetchone()
        email = user.get("email")
        password = user.get("password")
        self.id = id
        self.name = email
        self.password = password
    
def __repr__(self):
    return "%d/%s/%s" % (self.id, self.name, self.password)
class User(UserMixin):
    def __init__(self, email):
        cur, db = dbConnectDict()
        query = ("SELECT userID, password from tUser where email = '" + email + "';")
        cur.execute(query)
        user = cur.fetchone()
        userID = user.get("userID")
        password = user.get("password")
        self.id = userID
        self.name = email
        self.password = password
    
def __repr__(self):
    return "%d/%s/%s" % (self.id, self.name, self.password)