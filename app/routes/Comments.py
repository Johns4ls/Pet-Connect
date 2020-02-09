from Modules import Database
import datetime
from flask_login import login_required, current_user
from flask import redirect, request
from app import app
#Add a comment
@app.route('/Create/Comment/<int:postID>', methods=['GET', 'POST'])
def Comment(postID):
    postID = str(postID)
    Comment = request.form['Comment']
    session = Database.Session()
    Comment = Database.tComments(postID=postID, userID = current_user.id, Comment = Comment, ts=datetime.datetime.now(), image=None)
    session.add(Comment)
    session.commit()
    return redirect('/View/Post/'+postID)