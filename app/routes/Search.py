from app import app
from flask_login import login_required, current_user
from Modules import Database, Tlbx
from flask import request, session, render_template
@app.route('/Search', methods=['GET','POST'])
@login_required
def Search():
    db = Database.Session()
    Name = request.form['Search']
    session['Name'] = Name
    #Get top 5 most relevant dogs
    dogs = db.query(Database.tDog).filter(Database.tDog.name.contains(Name) | (Database.tDog.name.op('SOUNDS LIKE')(Name))).order_by(Database.tDog.name.match(Name).desc()).limit(5).all()
    followed = db.query(Database.tFollowers).filter(Database.tFollowers.userID == current_user.id)
    texts={}
    text =[]
    for dog in dogs:
        texts[dog.dogID] = 'Follow'
    for follower in followed:
        if follower.dogID in texts.keys():
            texts[follower.dogID] = 'Unfollow'
    for dog in dogs:
        text.append(texts[dog.dogID])

    #Get top 5 most relevant users
    Users = db.query(Database.tUser) \
        .filter(Database.tUser.firstName.contains(Name) | (Database.tUser.firstName.op('SOUNDS LIKE')(Name)) \
        | (Database.tUser.lastName.contains(Name) | (Database.tUser.lastName.op('SOUNDS LIKE')(Name)))) \
        .filter(Database.tUser.userID != current_user.id) \
        .order_by(Database.Match([Database.tUser.firstName, Database.tUser.lastName], Name)) \
        .limit(5).all()
    friended = db.query(Database.tFriend).filter(Database.tFriend.user == current_user.id)
    friends={}
    for user in Users:
        friends[user.userID] = 'Friend'
    for friend in friended:
        if friend.friend in friends.keys():
            friends[friend.friend] = 'Unfriend'
    return render_template('/Search/Search.html', results = zip(dogs, text), users = Users, friends = friends)

@app.route('/Search/Dogs', methods=['GET','POST'])
@login_required
def SearchDogs():
    db = Database.Session()
    Name = session.get('Name')
    #Get top 5 most relevant dogs and whether or not they are being followed.
    dogs = db.query(Database.tDog).filter(Database.tDog.name.contains(Name) | (Database.tDog.name.op('SOUNDS LIKE')(Name))).order_by(Database.tDog.name.match(Name).desc()).all()
    followed = db.query(Database.tFollowers).filter(Database.tFollowers.userID == current_user.id)
    texts={}
    text =[]
    for dog in dogs:
        texts[dog.dogID] = 'Follow'
    for follower in followed:
        if follower.dogID in texts.keys():
            texts[follower.dogID] = 'Unfollow'
    for dog in dogs:
        text.append(texts[dog.dogID])
    return render_template('/Search/SearchDogs.html', results = zip(dogs, text))

@app.route('/Search/Users', methods=['GET','POST'])
@login_required
def SearchUsers():
    db = Database.Session()
    Name = session.get('Name')
    Users = db.query(Database.tUser) \
        .filter(Database.tUser.firstName.contains(Name) | (Database.tUser.firstName.op('SOUNDS LIKE')(Name)) \
        | (Database.tUser.lastName.contains(Name) | (Database.tUser.lastName.op('SOUNDS LIKE')(Name)))) \
        .order_by(Database.Match([Database.tUser.email, Database.tUser.firstName, Database.tUser.lastName], Name)) \
        .all()
    return render_template('/Search/SearchUsers.html', Users = Users)