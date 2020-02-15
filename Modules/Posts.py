import Tlbx
import Database
import datetime 
from flask_login import current_user
from sqlalchemy.orm import aliased
def getPosts():
    session = Database.Session()
    tHostDog = aliased(Database.tDog, name="tHostDog")
    tGuestDog = aliased(Database.tDog, name="tGuestDog")
    Posts = session.query(Database.tPosts.postID, Database.tPosts.Post, Database.tDog, Database.tUser.userID, Database.tUser.firstName, Database.tUser.lastName, Database.tUser.image, Database.tPlayDate, tHostDog, tGuestDog)\
    .join(Database.tFollowers, Database.tPosts.dogID == Database.tFollowers.dogID) \
    .join(Database.tUser, Database.tPosts.userID == Database.tUser.userID) \
    .join(Database.tDog, Database.tPosts.dogID == Database.tDog.dogID) \
    .join(Database.tPlayDate, Database.tPosts.PlayDateID == Database.tPlayDate.PlayDateID) \
    .join(tHostDog, Database.tPlayDate.hostDogID == tHostDog.dogID) \
    .join(tGuestDog, Database.tPlayDate.guestDogID == tGuestDog.dogID) \
    .filter(Database.tFollowers.userID == current_user.id).order_by(Database.tPosts.postID.desc())
    return Posts