import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

#Connectors to database
def dbConnect():
  db = pymysql.connect(host='127.0.0.1', port=3306, user='Website', password='W3bsite!', db='PetConnect',autocommit=True)
  cur = db.cursor()
  return cur
def dbConnectDict():
  db = pymysql.connect(host='127.0.0.1', port=3306, user='Website', password='W3bsite!', db='PetConnect',autocommit=True)
  cur = db.cursor(pymysql.cursors.DictCursor)
  return cur

#Validate that the Email does not already exist
def validate_email(email):
    cur = dbConnect()
    cur.execute("SELECT email from tUser WHERE email = '" + email+"';")
    Result = cur.fetchall()
    if Result is not ():   
        return False

#Insert the new account information into the database
def new_Account(email, Password):
    cur = dbConnectDict()
    query = ("INSERT INTO tUser (email, password) VALUES ( %s, %s)")
    data = (email, Password)
    cur.execute(query, data)

#Get the password from the database
def getPass(email):
    cur = dbConnectDict()
    cur.execute("SELECT password from tUser where email ='" + email +"';")
    password = cur.fetchone()
    password = password.get("password")
    return password

#Hash the password before committing to the database
def hash_password(password):
    password = generate_password_hash(password)
    return password

#Check that the hash and the password entered are the same.
def check_password(email, password):
    return check_password_hash(getPass(email), password)