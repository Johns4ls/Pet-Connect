from Modules import Database
import datetime
def commitComment(userID, Comment):
    session = Database.Session()
    Comment = Database.tComments(postID=Comment.postID, userID = userID, Comment = Comment.Comment, ts=datetime.datetime.now(), image=None)
    session.add(Comment)
    session.commit()