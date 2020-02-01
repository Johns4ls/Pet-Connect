from app import app
from Modules import Tlbx, Database
from flask_login import login_required, current_user
from flask import render_template
#Initial screen upon entering website.
@app.route("/dashboard")
@login_required
def index():
    '''Do a normal select for comments and reacts. Then in jinja during the for loop for posts
    do a for loop for reacts and comments. Do an if post.postID == comment.postID and if post.postiD == react.postID'''
    session = Database.Session()
    currentUser = Tlbx.currentUserInfo(current_user.id)
    #Collect dogs in your family
    dogResults = session.query(Database.tDog).join(Database.tUser, Database.tDog.familyID == Database.tUser.familyID).filter(Database.tUser.userID == current_user.id)

    #Get comments of posts
    commentResults = session.query(Database.tPosts.postID, Database.tComments.Comment, Database.tUser.userID, Database.tUser.firstName, Database.tUser.lastName, Database.tUser.image) \
        .join(Database.tUser, Database.tComments.userID == Database.tUser.userID)\
        .join(Database.tPosts, Database.tComments.postID == Database.tPosts.postID).order_by(Database.tComments.commentID.desc())

    #Get reacts of posts
    reactResults = session.query(Database.tReacts.postID, Database.tUser.userID, Database.tUser.firstName, Database.tUser.lastName, Database.tUser.image) \
        .join(Database.tUser, Database.tReacts.userID == Database.tUser.userID)\
        .join(Database.tPosts, Database.tReacts.postID == Database.tPosts.postID)

    #Get Posts
    postResults = session.query(Database.tPosts.postID, Database.tPosts.Post, Database.tDog, Database.tUser.userID, Database.tUser.firstName, Database.tUser.lastName, Database.tUser.image)\
    .join(Database.tFollowers, Database.tPosts.dogID == Database.tFollowers.dogID) \
    .join(Database.tUser, Database.tPosts.userID == Database.tUser.userID) \
    .join(Database.tDog, Database.tPosts.dogID == Database.tDog.dogID) \
    .filter(Database.tFollowers.userID == current_user.id).order_by(Database.tPosts.postID.desc())
    yourReacts = session.query(Database.tReacts.postID).filter(Database.tReacts.userID == current_user.id)

    likes={}
    like =[]
    for react in postResults:
        likes[react.postID] = 'Like'
    for yourReact in yourReacts:
        if yourReact.postID in likes.keys():
            likes[yourReact.postID] = 'Unlike'
    for react in postResults:
        like.append(likes[react.postID])
    return render_template('HomePage/Dashboard.html', currentUser = currentUser, dogResults = dogResults, \
        postResults = zip(postResults, like), commentResults = commentResults, reactResults = reactResults)