from app import app
from Modules import Tlbx, Database
from flask import render_template
from flask_login import current_user
@app.route('/User/Profile/<int:userID>', methods=['GET', 'POST'])
def userProfile(userID):
    session = Database.Session()
    user = session.query(Database.tUser).filter(Database.tUser.userID == userID)
    for user in user:
        user = user

    #Get comments of posts
    commentResults = session.query(Database.tPosts.postID, Database.tComments.Comment, Database.tUser.userID, Database.tUser.firstName, Database.tUser.lastName, Database.tUser.image) \
        .join(Database.tUser, Database.tComments.userID == Database.tUser.userID)\
        .join(Database.tPosts, Database.tComments.postID == Database.tPosts.postID)

    #Get reacts of posts
    reactResults = session.query(Database.tReacts.postID, Database.tUser.userID, Database.tUser.firstName, Database.tUser.lastName, Database.tUser.image) \
        .join(Database.tUser, Database.tReacts.userID == Database.tUser.userID)\
        .join(Database.tPosts, Database.tReacts.postID == Database.tPosts.postID)

    #Get Posts
    postResults = session.query(Database.tPosts.postID, Database.tPosts.Post, Database.tDog, Database.tUser.userID, Database.tUser.firstName, Database.tUser.lastName, Database.tUser.image)\
    .join(Database.tFollowers, Database.tPosts.dogID == Database.tFollowers.dogID) \
    .join(Database.tUser, Database.tPosts.userID == Database.tUser.userID) \
    .join(Database.tDog, Database.tPosts.dogID == Database.tDog.dogID) \
    .filter(Database.tPosts.userID == userID).order_by(Database.tPosts.postID.desc())
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

    #Collect dogs in your family
    dogResults = session.query(Database.tDog).join(Database.tUser, Database.tDog.familyID == Database.tUser.familyID).filter(Database.tUser.userID == userID)
    return render_template('Account/Profile.html', user = user, dogResults = dogResults, postResults = zip(postResults, like), commentResults = commentResults, reactResults = reactResults)

@app.route('/Dog/Profile/<int:dogID>', methods=['GET', 'POST'])
def dogProfile(dogID):
    session = Database.Session()
    #Get information about the dog
    dog = session.query(Database.tDog, Database.tBreed).filter(Database.tDog.dogID == dogID) \
    .join(Database.tBreed, Database.tBreed.breedID == Database.tDog.dogID)
    for dog in dog:
        dog = dog

    #Get comments of posts
    commentResults = session.query(Database.tPosts.postID, Database.tComments.Comment, Database.tUser.userID, Database.tUser.firstName, Database.tUser.lastName, Database.tUser.image) \
        .join(Database.tUser, Database.tComments.userID == Database.tUser.userID)\
        .join(Database.tPosts, Database.tComments.postID == Database.tPosts.postID)

    #Get reacts of posts
    reactResults = session.query(Database.tReacts.postID, Database.tUser.userID, Database.tUser.firstName, Database.tUser.lastName, Database.tUser.image) \
        .join(Database.tUser, Database.tReacts.userID == Database.tUser.userID)\
        .join(Database.tPosts, Database.tReacts.postID == Database.tPosts.postID)

    #Get Posts
    postResults = session.query(Database.tPosts.postID, Database.tPosts.Post, Database.tDog, Database.tUser.userID, Database.tUser.firstName, Database.tUser.lastName, Database.tUser.image)\
    .join(Database.tFollowers, Database.tPosts.dogID == Database.tFollowers.dogID) \
    .join(Database.tUser, Database.tPosts.userID == Database.tUser.userID) \
    .join(Database.tDog, Database.tPosts.dogID == Database.tDog.dogID) \
    .filter(Database.tFollowers.dogID == dogID).order_by(Database.tPosts.postID.desc())

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

    return render_template('Account/DogProfile.html', postResults = zip(postResults, like), commentResults = commentResults, reactResults = reactResults, yourReacts = yourReacts, dog=dog)

@app.route('/Dog/Info/<int:dogID>', methods=['GET', 'POST'])
def dogInfo(dogID):
    session = Database.Session()
    user = session.query(Database.tUser).filter(Database.tUser.userID == current_user.id)
    for user in user:
        user = user
    #Collect dogs in your family
    dog = session.query(Database.tDog, Database.tBreed, Database.tFavoriteToy).filter(Database.tDog.dogID == dogID) \
    .join(Database.tBreed, Database.tBreed.breedID == Database.tDog.dogID) \
    .join(Database.tFavoriteToy, Database.tDog.favToyID == Database.tFavoriteToy.favToyID)
    for dog in dog:
        dog = dog

    return render_template('Account/DogInfo.html', dog = dog)
