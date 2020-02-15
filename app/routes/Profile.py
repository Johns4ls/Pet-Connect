from app import app
from Modules import Tlbx, Database, Comments, Reacts, Posts
from flask import render_template
from flask_login import current_user
@app.route('/User/Profile/<int:userID>', methods=['GET', 'POST'])
def userProfile(userID):
    session = Database.Session()
    user = session.query(Database.tUser).filter(Database.tUser.userID == userID)
    for user in user:
        user = user

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


    cur, db = Tlbx.dbConnectDict()
    query = "select tFamily.familyID from tFamily \
        JOIN tUser on tFamily.familyID = tUser.familyID \
        JOIN tDog on tUser.familyID = tDog.familyID \
        WHERE tUser.userID = %s AND tDog.dogID = %s;"
    data = (current_user.id, dogID)
    cur.execute(query, data)
    family = cur.fetchone()
    if(family is not None):
        return render_template('Account/AdminDogProfile.html', postResults = zip(postResults, like), commentResults = commentResults, reactResults = reactResults, yourReacts = yourReacts, dog=dog)
    else:
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
