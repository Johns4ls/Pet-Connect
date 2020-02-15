from Modules import Database
import datetime
def commitComment(userID, Comment):
    session = Database.Session()
    Comment = Database.tComments(postID=Comment['postID'], userID = userID, Comment = Comment['Comment'], ts=datetime.datetime.now(), image=None)
    session.add(Comment)
    session.commit()

def getComments():
    session = Database.Session()
    commentResults = session.query(Database.tPosts.postID, Database.tComments.Comment, Database.tUser.userID, Database.tUser.firstName, Database.tUser.lastName, Database.tUser.image) \
    .join(Database.tUser, Database.tComments.userID == Database.tUser.userID)\
    .join(Database.tPosts, Database.tComments.postID == Database.tPosts.postID).order_by(Database.tComments.commentID.desc())
    return commentResults