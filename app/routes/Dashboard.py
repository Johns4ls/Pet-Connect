from app import app
from Modules import Tlbx, Database, Comments, Reacts, Posts
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
    commentResults = Comments.getComments()

    #Get reacts of posts
    reactResults = Reacts.getReacts()
    yourReacts = Reacts.yourReacts()

    #Get Posts
    postResults = Posts.getPosts()

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