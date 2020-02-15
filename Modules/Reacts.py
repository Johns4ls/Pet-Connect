import Tlbx
import Database
import datetime 
from flask_login import current_user

def getReacts():
    session = Database.Session()
    Reacts = session.query(Database.tReacts.postID, Database.tUser.userID, Database.tUser.firstName, Database.tUser.lastName, Database.tUser.image) \
            .join(Database.tUser, Database.tReacts.userID == Database.tUser.userID)\
            .join(Database.tPosts, Database.tReacts.postID == Database.tPosts.postID)
    return Reacts

def yourReacts():
        session = Database.Session()
        yourReacts = session.query(Database.tReacts.postID).filter(Database.tReacts.userID == current_user.id)
        return yourReacts