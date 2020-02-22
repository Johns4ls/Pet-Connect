from app import app
from Modules import Database
from flask_login import login_required, current_user
from flask import redirect
import datetime
@app.route('/Like/<int:postID>', methods=['GET', 'POST'])
def Like(postID):
    postID=str(postID)
    session = Database.Session()
    Like = Database.tReacts(userID=current_user.id, postID=postID, ts=datetime.datetime.now())
    session.add(Like)
    session.commit()
    return '', 204

#Remove a like
@app.route('/Unlike/<int:postID>', methods=['GET', 'POST'])
def Unlike(postID):
    postID=str(postID)
    session = Database.Session()
    session.query(Database.tReacts).filter(Database.tReacts.postID==postID) \
    .filter(Database.tReacts.userID==current_user.id).delete()
    session.commit()
    return '', 204