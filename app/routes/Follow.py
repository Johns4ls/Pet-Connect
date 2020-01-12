from app import app
from Modules import Database
from flask_login import login_required, current_user
@app.route('/Follow/<int:dogID>', methods=['GET','POST'])
@login_required
def FollowDogs(dogID):
   session = Database.Session()
   addFollower = Database.tFollowers(dogID = dogID, userID= current_user.id)
   session.add(addFollower)
   session.commit()
   return '', 204

@app.route('/Unfollow/<int:dogID>', methods=['GET','POST'])
@login_required
def UnfollowDogs(dogID):
    session = Database.Session()
    session.query(Database.tFollowers).filter(Database.tFollowers.dogID==dogID) \
    .filter(Database.tFollowers.userID==current_user.id).delete()
    session.commit()
    return '', 204