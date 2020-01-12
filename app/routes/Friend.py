from app import app
from Modules import Database
from flask_login import login_required, current_user
@app.route('/Friend/<int:userID>', methods=['GET','POST'])
@login_required
def AddFriend(userID):
    session = Database.Session()
    addFriend = Database.tFriend(friend = current_user.id, user = userID)
    addUser = Database.tFriend(user = current_user.id, friend = userID)
    session.add(addFriend)
    session.add(addUser)
    session.commit()
    return('', 204)

@app.route('/Unfriend/<int:userID>', methods=['GET','POST'])
@login_required
def UnFriend(userID):
    session = Database.Session()
    session.query(Database.tFriend) \
        .filter(Database.tFriend.user == userID) \
        .filter(Database.tFriend.friend == current_user.id) \
        .delete()
    session.query(Database.tFriend) \
        .filter(Database.tFriend.user == current_user.id) \
        .filter(Database.tFriend.friend == userID) \
        .delete()
    session.commit()
    return('', 204)