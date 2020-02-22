from Modules import Database, Tlbx
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

def getPostComments(postID):
    cur, db = Tlbx.dbConnectDict()
    query = "SELECT tPosts.postID, tComments.Comment, tUser.userID, tUser.firstName, tUser.lastName, tUser.image \
    FROM tComments INNER JOIN tUser ON tComments.userID = tUser.userID INNER JOIN tPosts ON tComments.postID = tPosts.postID \
    WHERE tPosts.postID = %s ORDER BY tComments.commentID DESC LIMIT 3;"
    data = (postID)
    cur.execute(query, data)
    commentResults = cur.fetchall()
    return commentResults