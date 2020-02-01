from app import app
from Modules import Database, Tlbx
import datetime
from flask import redirect, request, render_template, flash
from flask_login import current_user, login_required
@app.route('/Create/Post', methods=['GET','POST'])
@login_required
def CreatePost():
    session = Database.Session()
    dogID = request.form['DogValue']
    Post = request.form['Post']
    Query = Database.tPosts(dogID=dogID, userID=current_user.id, Post=Post, ts=datetime.datetime.now(), image=None)
    session.add(Query)
    session.commit()
    flash('Posted successfully')
    return redirect('/dashboard')
@app.route('/Likes/Post/<int:postID>', methods=['GET','POST'])
def likes(postID):
    session = Database.Session()
    Reacts = session.query(Database.tUser).join(Database.tReacts, Database.tReacts.userID == Database.tUser.userID) \
    .filter(Database.tReacts.postID==postID)
    return render_template('/Likes/Likes.html', Reacts = Reacts)

@app.route('/View/Post/<int:postID>', methods=['GET','POST'])
def viewPost(postID):
    session = Database.Session()
    #Get post information
    post = session.query(Database.tPosts.postID, Database.tPosts.Post, Database.tDog.name, Database.tUser.firstName, Database.tUser.lastName) \
    .join(Database.tUser, Database.tPosts.userID == Database.tUser.userID) \
    .join(Database.tDog, Database.tDog.dogID == Database.tPosts.dogID) \
    .filter(Database.tPosts.postID==postID)
    for post in post:
        post = post
        #Get comments of posts
    comments = session.query( Database.tComments.Comment, Database.tUser.firstName, Database.tUser.lastName) \
        .join(Database.tUser, Database.tComments.userID == Database.tUser.userID) \
        .join(Database.tPosts, Database.tComments.postID == Database.tPosts.postID) \
        .filter(Database.tPosts.postID == postID)

    #Get reacts of posts
    reacts = session.query(Database.tReacts.reactID, Database.tUser.firstName, Database.tUser.lastName) \
        .join(Database.tUser, Database.tReacts.userID == Database.tUser.userID) \
        .join(Database.tPosts, Database.tReacts.postID == Database.tPosts.postID) \
        .filter(Database.tPosts.postID == postID)

    yourReacts = session.query(Database.tReacts.postID).filter(Database.tReacts.userID == current_user.id) \
        .filter(Database.tReacts.postID == postID)
    yourLike = None
    for yourLike in yourReacts:
        yourLike = yourLike
    if yourLike is not None:
        like = "Unlike"
    else:
        like = "Like"

    cur, db = Tlbx.dbConnectDict()
    query = "UPDATE tUser \
    SET last_message_read_time = %s \
    WHERE userID = %s;"
    data = (datetime.datetime.now(), current_user.id)
    cur.execute(query, data)

    return render_template('/post/Post.html', like = like, post = post, comments = comments, reacts = reacts)