import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, UserMixin
import os
from PIL import Image, ExifTags
import Database
from Database import *
import datetime

#Connectors to database
def dbConnect():
    if os.name == "nt":
        db = pymysql.connect(host='127.0.0.1', port=3306, user='Website', password='W3bsite!', db='PetConnect',autocommit=True)
    else:
        db = pymysql.connect(host='ec2-52-14-47-9.us-east-2.compute.amazonaws.com', port=3306, user='Website', password='W3bsite!', db='PetConnect',autocommit=True)
    cur = db.cursor()
    return cur
def dbConnectDict():
    if os.name == "nt":
        db = pymysql.connect(host='127.0.0.1', port=3306, user='Website', password='W3bsite!', db='PetConnect',autocommit=True)
    else:
        db = pymysql.connect(host='ec2-52-14-47-9.us-east-2.compute.amazonaws.com', port=3306, user='Website', password='W3bsite!', db='PetConnect',autocommit=True)
    cur = db.cursor(pymysql.cursors.DictCursor)
    return cur, db

#Validate that the Email does not already exist
def validate_email(email):
    cur= dbConnect()
    cur.execute("SELECT email from tUser WHERE email = '" + email+"';")
    Result = cur.fetchall()
    if Result is not ():
        return False


def imgToJPG(location, image):
    if os.name == 'nt':
        dirpath = os.getcwd()
    else:
        dirpath = '/home/ec2-user/official-repo/Pet-Connect'
    path =  'pictures/' + location + '/'
    imageName = image.filename.split('.')
    imageType = imageName[1]
    imageName = imageName[0]
    fullPath =  path + imageName
    savePath = dirpath + '/app/static/pictures/' + location + '/' + imageName
    thumbPath =  savePath
    try:
        if imageName != '' and not os.path.exists(fullPath):
            image = Image.open(image.stream)
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation]=='Orientation':
                    break
            exif=dict(image._getexif().items())
            if exif[orientation] == 3:
                image=image.rotate(180, expand=True)
            elif exif[orientation] == 6:
                image=image.rotate(270, expand=True)
            elif exif[orientation] == 8:
                image=image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # cases: image doesn't have getexif
        pass
    savePath = savePath +  ".jpg"
    print(imageType)
    if imageType == 'PNG' or 'png':
        image = image.convert('RGB')
    image.save(savePath,optimize=True,quality=80)
    if location == "Profile":
        thumbnailGen(image, thumbPath)
    else:
        fullPath = None
    return fullPath

def thumbnailGen(image, path):
    size = 128, 128
    image.thumbnail(size)
    print(path)
    image.save(path + ".thumbnail", "JPEG" )


#Insert the new account information into the database
def new_Account(firstName, lastName, email, password, address, city, state, image):
    cur, db = dbConnectDict()
    addressQuery = ("INSERT INTO tAddress (address, city, state) VALUES(%s, %s, %s);")
    data = (address, city, state)
    cur.execute(addressQuery, data)
    userQuery = ("INSERT INTO tUser (firstName, lastName, email, familyID, password, image, addressID) VALUES(%s, %s, %s, NULL, %s, %s, LAST_INSERT_ID());")
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

def currentUserInfo(userID):
    session = Database.Session()
    user = session.query(Database.tUser).filter(Database.tUser.userID == userID)
    for user in user:
        user = user
    return user

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
