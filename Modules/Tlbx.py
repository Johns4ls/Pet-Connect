import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, UserMixin
import os
from PIL import Image, ExifTags

#Connectors to database
def dbConnect():

    #db = pymysql.connect(host='ec2-13-59-203-226.us-east-2.compute.amazonaws.com', port=3306, user='Website', password='W3bsite!', db='PetConnect',autocommit=True)
    db = pymysql.connect(host='127.0.0.1', port=3306, user='Website', password='W3bsite!', db='PetConnect',autocommit=True)
    cur = db.cursor()
    return cur
def dbConnectDict():
  #db = pymysql.connect(host='ec2-13-59-203-226.us-east-2.compute.amazonaws.com', port=3306, user='Website', password='W3bsite!', db='PetConnect',autocommit=True)
    db = pymysql.connect(host='127.0.0.1', port=3306, user='Website', password='W3bsite!', db='PetConnect',autocommit=True)
    cur = db.cursor(pymysql.cursors.DictCursor)
    return cur, db

#Validate that the Email does not already exist
def validate_email(email):
    cur= dbConnect()
    cur.execute("SELECT email from tUser WHERE email = '" + email+"';")
    Result = cur.fetchall()
    if Result is not ():
        return False


def imgToPNG(location, image):
    dirpath = os.getcwd()
    path = dirpath + '/static/pictures/' + location + '/'
    imageName = image.filename.split('.')
    imageName = imageName[0]
    png = dirpath + imageName + ".png"
    if imageName != '' and not os.path.exists(png):
        imageName = path + image
        image = Image.open(image.stream)
        if hasattr(image, '_getexif'):
            orientation = 0x0112
            exif = image._getexif()
            if exif is not None:
                orientation = exif[orientation]
                rotations = {
                    3: Image.ROTATE_180,
                    6: Image.ROTATE_270,
                    8: Image.ROTATE_90
                }
                if orientation in rotations:
                    image = image.transpose(rotations[orientation])

        image.save(png,optimize=True,quality=85)

#Insert the new account information into the database
def new_Account(firstName, lastName, email, password, address, city, state, zipCode, image):
    cur, db = dbConnectDict()
    addressQuery = ("INSERT INTO tAddress (address, city, state, zip) VALUES(%s, %s, %s, %s);")
    data = (address, city, state, zipCode)
    cur.execute(addressQuery, data)
    userQuery = ("INSERT INTO tUser (firstName, lastName, email, familyID, password, image, addressID) VALUES(%s, %s, %s, NULL, %s, %s, LAST_INSERT_ID());")
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
