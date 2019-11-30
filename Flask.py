#Various imports
from flask import Flask, flash, render_template, redirect, session, request
from werkzeug.utils import secure_filename
from Modules.forms import LoginForm, RegisterForm, UserInfoForm, CreateFamilyForm, CreateDogForm, FavoriteParkForm, PasswordResetForm
from Modules import Tlbx, Database
from flask_sqlalchemy import SQLAlchemy, functools
from sqlalchemy import and_, or_
from sqlalchemy.orm import aliased
from flask_login import LoginManager, login_required, logout_user, current_user
import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
'''Secret to prevent Cross-Site Request Forgery(CSRF) attacks.
   This will need to be updated before the site goes live.'''
app.secret_key = 'some_secret'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/"

@login_manager.user_loader
def load_user(userid):
    return Tlbx.userRefresh(userid)
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
    commentResults = session.query(Database.tPosts.postID, Database.tComments.Comment, Database.tUser.userID, Database.tUser.firstName, Database.tUser.lastName) \
        .join(Database.tUser, Database.tComments.userID == Database.tUser.userID)\
        .join(Database.tPosts, Database.tComments.postID == Database.tPosts.postID)

    #Get reacts of posts
    reactResults = session.query(Database.tReacts.postID, Database.tUser.userID, Database.tUser.firstName, Database.tUser.lastName) \
        .join(Database.tUser, Database.tReacts.userID == Database.tUser.userID)\
        .join(Database.tPosts, Database.tReacts.postID == Database.tPosts.postID)

    #Get Posts
    postResults = session.query(Database.tPosts.postID, Database.tPosts.Post, Database.tDog.dogID, Database.tDog.name, Database.tUser.userID, Database.tUser.firstName, Database.tUser.lastName)\
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

    #Get unread messages
    #messages = Database.new_messages(current_user.id)
    #print(messages)
    count, notifications = Tlbx.getNotifications(current_user.id)
    return render_template('HomePage/Dashboard.html', count = count, notifications = notifications, currentUser = currentUser, dogResults = dogResults, postResults = zip(postResults, like), commentResults = commentResults, reactResults = reactResults)

#Renders the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/dashboard')
    #instantiates the forms to login and register your account
    Loginform = LoginForm()
    Registerform = RegisterForm()

    #Checks to ensure fields are not null
    if Loginform.validate_on_submit():
        #Checks to ensure username and password are correct.
        if(Tlbx.check_password(Loginform.email.data, Loginform.password.data) is not False):
            Tlbx.loginUser(Loginform.email.data)
            return redirect('/dashboard')
        flash("Email or Password is incorrect.")
    return render_template('Login/login.html', Registerform=Registerform, Loginform=Loginform)

#Start registration on landing page
@app.route('/register', methods=['GET', 'POST'])
def register():
    Registerform = RegisterForm()
    Loginform = LoginForm()
    if Registerform.validate_on_submit():
        session['email'] = Registerform.email.data
        session['password'] = Registerform.password.data
        if(Tlbx.validate_email(Registerform.email.data) is not False):
            UserInfoform = UserInfoForm()
            return render_template('Register/userInfo.html', UserInfoform = UserInfoform )
        flash('Email address already exists')
        return redirect('/')


    return render_template('Login/login.html', Registerform=Registerform, Loginform=Loginform)

#Create a new User
@app.route('/Create/User', methods=['GET', 'POST'])
def userInfo():
    UserInfoform = UserInfoForm()
    if UserInfoform.validate_on_submit():
        firstName = UserInfoform.firstName.data
        lastName = UserInfoform.lastName.data
        email = session.get('email')
        password =  Tlbx.hash_password(session.get('password', None))
        address = UserInfoform.address.data
        city = UserInfoform.city.data
        state = UserInfoform.state.data
        zipCode = UserInfoform.zipCode.data
        image = request.files[UserInfoform.profileImage.name]
        image = Tlbx.imgToJPG("Profile", image)
        Tlbx.new_Account(firstName, lastName, email, password, address, city, state, zipCode, image)
        Tlbx.loginUser(email)
        return render_template('/Family/FamilySplash.html')
    flash("Please input data in all fields")
    return render_template('Register/userInfo.html', UserInfoform = UserInfoform)

#Add a like
@app.route('/Like/<int:postID>', methods=['GET', 'POST'])
def Like(postID):
    postID=str(postID)
    session = Database.Session()
    Like = Database.tReacts(userID=current_user.id, postID=postID, ts=datetime.datetime.now())
    session.add(Like)
    session.commit()
    return redirect('/dashboard')

#Remove a like
@app.route('/Unlike/<int:postID>', methods=['GET', 'POST'])
def Unlike(postID):
    postID=str(postID)
    session = Database.Session()
    session.query(Database.tReacts).filter(Database.tReacts.postID==postID) \
    .filter(Database.tReacts.userID==current_user.id).delete()
    session.commit()
    return redirect('/dashboard')

#Add a comment
@app.route('/Create/Comment/<int:postID>', methods=['GET', 'POST'])
def Comment(postID):
    postID = str(postID)
    Comment = request.form['Comment']
    session = Database.Session()
    Comment = Database.tComments(postID=postID, userID = current_user.id, Comment = Comment, ts=datetime.datetime.now(), image=None)
    session.add(Comment)
    session.commit()
    return redirect('/dashboard')

@app.route('/forgotPass', methods=['GET', 'POST'])
def forgotPass():
    PasswordResetform = PasswordResetForm()
    # grab data from form
    email = PasswordResetform.email.data
    password = PasswordResetform.password.data
    confirmpassword = PasswordResetform.passwordConfirm.data
    return render_template('PasswordReset/PasswordReset.html', PasswordResetform = PasswordResetform)

@app.route('/PasswordReset', methods=['GET','POST'])
def passwordReset():
    print("WIP")

@app.route('/Create/Start/Family', methods=['GET','POST'])
@login_required
def CreateNewFamily():
    CreateFamilyform = CreateFamilyForm()
    return render_template('/Family/FamilyCreate.html', CreateFamilyform = CreateFamilyform )

@app.route('/Create/Finish/Family', methods=['GET','POST'])
@login_required
def familyCreation():
    sqlalch = Database.Session()
    HeadOfHouse = Database.tHeadofHouse(userID = current_user.id)
    sqlalch.add(HeadOfHouse)
    id = sqlalch.commit()
    CreateFamilyform = CreateFamilyForm()
    if CreateFamilyform.validate_on_submit():
        CreateDogform = CreateDogForm()
        familyName = CreateFamilyform.surName.data
        cur, db = Tlbx.dbConnectDict()
        cursor= Database.Session()
        query = ("INSERT INTO tFamily (familyName, headofHouseID) VALUES(%s, %s);")
        data = (familyName, id)
        cur.execute(query, data)
        session['familyID'] = db.insert_id()
        x = cursor.query(Database.tUser).get(current_user.id)
        x.familyID = db.insert_id()
        cursor.commit()
        currentUser = Tlbx.currentUserInfo(current_user.id)
        return render_template('Dog/NewDog.html', CreateDogform = CreateDogform, currentUser = currentUser)
    flash("Please add a family name")
    return render_template('/Family/FamilyCreate.html', CreateFamilyform = CreateFamilyform )


@app.route('/Join/Family/Landing', methods=['GET','POST'])
@login_required
def JoinFamilyLanding():
    return render_template('/Family/JoinFamily.html')

@app.route('/Join/Family/Search', methods=['GET','POST'])
@login_required
def JoinFamilySearch():
    session = Database.Session()
    Name = request.form['Search']
    Users = session.query(Database.tUser).join(Database.tHeadofHouse, Database.tHeadofHouse.userID == Database.tUser.userID) \
        .filter(Database.tUser.email.contains(Name) | (Database.tUser.email.op('SOUNDS LIKE')(Name))).order_by(Database.tUser.email.match(Name).desc()).all()

    return render_template('/Family/JoinFamilySearch.html', Users = Users)

@app.route('/Join/Family/<int:userID>', methods=['GET','POST'])
@login_required
def JoinFamily(userID):
    session = Database.Session()
    familyID = session.query(Database.tUser.familyID).filter(Database.tUser.userID == userID)
    for family in familyID:
        familyID = family.familyID
    x = session.query(Database.tUser).get(current_user.id)
    x.familyID = familyID
    session.commit()
    dogIDs = session.query(Database.tDog.dogID).filter(Database.tDog.familyID == familyID)
    for dogID in dogIDs:
        dog = Database.tFollowers(dogID = dogID.dogID, userID = current_user.id)
        session.add(dog)
        session.commit()
    return redirect('/dashboard')

@app.route('/Follow/<int:dogID>', methods=['GET','POST'])
@login_required
def FollowDogs(dogID):
   session = Database.Session()
   addFollower = Database.tFollowers(dogID = dogID, userID= current_user.id)
   session.add(addFollower)
   session.commit()
   return '', 204

@app.route('/Unfollow/<int:dogID>', methods=['GET','POST'])
@login_required
def UnfollowDogs(dogID):
    session = Database.Session()
    session.query(Database.tFollowers).filter(Database.tFollowers.dogID==dogID) \
    .filter(Database.tFollowers.userID==current_user.id).delete()
    session.commit()
    return '', 204

@app.route('/Likes/Post/<int:postID>', methods=['GET','POST'])
def likes(postID):
    session = Database.Session()
    Reacts = session.query(Database.tUser).join(Database.tReacts, Database.tReacts.userID == Database.tUser.userID) \
    .filter(Database.tReacts.postID==postID)
    count, notifications = Tlbx.getNotifications(current_user.id)
    return render_template('/Likes/Likes.html', Reacts = Reacts, count = count, notifications = notifications)

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

    count, notifications = Tlbx.getNotifications(current_user.id)
    currentUser = Tlbx.currentUserInfo(current_user.id)
    return render_template('/post/Post.html', like = like, count = count, notifications = notifications, currentUser = currentUser, post = post, comments = comments, reacts = reacts)


@app.route('/Friend/<int:userID>', methods=['GET','POST'])
@login_required
def AddFriend(userID):
    session = Database.Session()
    addFriend = Database.tFriend(friend = current_user.id, user = userID)
    addUser = Database.tFriend(user = current_user.id, friend = userID)
    session.add(addFriend)
    session.add(addUser)
    session.commit()
    return('', 204)

@app.route('/Friend/<int:userID>', methods=['GET','POST'])
@login_required
def UnFriend(userID):
    session = Database.Session()
    session.query(Database.tFriend) \
        .filter(Database.tFriend.user == userID) \
        .filter(Database.tFriend.friend == current_user.id) \
        .delete()
    session.query(Database.tFriend) \
        .filter(Database.tFriend.user == current_user.id) \
        .filter(Database.tFriend.friend == userID) \
        .delete()
    session.commit()
    return('', 204)

@app.route('/Send/Message/<int:userID>', methods=['GET','POST'])
@login_required
def sendMessage(userID):
    #user userID to get both friendIDs to submit messages
    
    #Get both friendIDs associated with friendship
    cur, db = Tlbx.dbConnectDict()
    query = ("SELECT friendID from tFriend \
        WHERE tFriend.user = %s \
        AND tFriend.friend = %s;")
    data = (current_user.id, userID)
    cur.execute(query, data)
    UserFriendID = cur.fetchone()
    data = (userID, current_user.id)
    cur.execute(query, data)
    FriendFriendID = cur.fetchone()
    session = Database.Session()
    message = request.form['message']

    addMessageFriend = Database.tMessage(friendID = FriendFriendID['friendID'], sender = current_user.id, \
        recipient = userID, time_Sent = datetime.datetime.now(), message = message)
    
    addMessageUser = Database.tMessage(friendID = UserFriendID['friendID'], sender = current_user.id, \
        recipient = userID, time_Sent = datetime.datetime.now(), message = message)


    session.add(addMessageUser)
    session.add(addMessageFriend)
    session.commit()

    return redirect('/Messages')



@app.route('/Messages', methods=['GET','POST'])
@login_required
def Messages():

    #Get all messages from you and your friends. Also need friendID to link it up with jinja
    friends, db = Tlbx.dbConnectDict()
    friendQuery = ("Select friendID, tUser.userID, tUser.firstName, tUser.lastName, tUser.image from tFriend \
        JOIN tUser ON tFriend.friend = tUser.userID \
        WHERE tFriend.user = %s;")
    data = (current_user.id)
    friends.execute(friendQuery, data)
    #Still need to orderby timestamp
    messageQuery = ("Select tMessage.friendID, tMessage.message, tMessage.time_Sent, tMessage.recipient, tUser.firstName, tUser.lastName from tMessage \
        JOIN tFriend ON tFriend.friendID = tMessage.friendID \
        JOIN tUser ON tFriend.friend = tUser.userID \
        WHERE tFriend.user = %s")
    cur, db = Tlbx.dbConnectDict()
    data = (current_user.id)
    cur.execute(messageQuery, data)
    currentUser = Tlbx.currentUserInfo(current_user.id)
    count, notifications = Tlbx.getNotifications(current_user.id)
    return render_template('/Messages/Messages.html', messages = cur.fetchall(), friends = friends.fetchall(), currentUser=currentUser, count = count, notifications = notifications)

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

    currentUser = Tlbx.currentUserInfo(current_user.id)

    #Get top 5 most relevant users
    Users = db.query(Database.tUser) \
        .filter(Database.tUser.firstName.contains(Name) | (Database.tUser.firstName.op('SOUNDS LIKE')(Name)) \
        | (Database.tUser.lastName.contains(Name) | (Database.tUser.lastName.op('SOUNDS LIKE')(Name)))) \
        .order_by(Database.Match([Database.tUser.firstName, Database.tUser.lastName], Name)) \
        .limit(5).all()

    count, notifications = Tlbx.getNotifications(current_user.id)
    return render_template('/Search/Search.html', results = zip(dogs, text), Users = Users, currentUser = currentUser, count = count, notifications = notifications)

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
    currentUser = Tlbx.currentUserInfo(current_user.id)
    count, notifications = Tlbx.getNotifications(current_user.id)
    return render_template('/Search/SearchDogs.html', results = zip(dogs, text), currentUser = currentUser, count = count, notifications = notifications)

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
    currentUser = Tlbx.currentUserInfo(current_user.id)
    count, notifications = Tlbx.getNotifications(current_user.id)
    return render_template('/Search/SearchUsers.html', Users = Users, currentUser = currentUser, count = count, notifications = notifications)

@app.route('/Create/New/Dog', methods=['GET','POST'])
@login_required
def CreateNewDog():
    currentUser = Tlbx.currentUserInfo(current_user.id)
    session = Database.Session()
    headOfHouse = session.query(Database.tHeadofHouse).filter(Database.tHeadofHouse.userID == current_user.id).all()
    if headOfHouse == []:
        flash("You must be the head of household to create a new dog")
        return redirect('/dashboard')
    followed = session.query(Database.tDog.dogID).join(Database.tUser, Database.tDog.familyID == Database.tUser.familyID) \
    .filter(Database.tUser.userID == current_user.id)
    CreateDogform = CreateDogForm()
    count, notifications = Tlbx.getNotifications(current_user.id)
    if followed is not None:
        return render_template('Dog/NewDog.html', currentUser = currentUser, CreateDogform = CreateDogform, count = count, notifications = notifications)
    else:
        return render_template('Dog/Initial_NewDog.html', CreateDogForm = CreateDogform)

@app.route('/Create/Start/Park', methods=['GET','POST'])
@login_required
def StartPark():
    CreateDogform = CreateDogForm()
    dbsession = Database.Session()
    if CreateDogform.validate_on_submit():
        session['dogName'] = CreateDogform.dogName.data
        session['gender'] = CreateDogform.gender.data
        session['breed'] = CreateDogform.breed.data
        session['fixed'] = CreateDogform.fixed.data
        session['age'] = CreateDogform.age.data
        session['favToy'] = CreateDogform.favToy.data
        session['size'] = CreateDogform.size.data
        session['weight'] = CreateDogform.weight.data
        session['bio'] = CreateDogform.bio.data
        image = request.files[CreateDogform.profileImage.name]
        session['image'] = Tlbx.imgToJPG("Profile", image)
        FavoriteParkform = FavoriteParkForm()
        followed = dbsession.query(Database.tDog.dogID).join(Database.tUser, Database.tDog.familyID == Database.tUser.familyID) \
        .filter(Database.tUser.userID == current_user.id)
        count, notifications = Tlbx.getNotifications(current_user.id)
        currentUser = Tlbx.currentUserInfo(current_user.id)
        if followed is not None:
            return render_template('/Dog/NewPark.html', currentUser = currentUser, FavoriteParkform = FavoriteParkform, count = count, notifications = notifications)
        else:
            return render_template('Dog/Initial_NewPark.html', FavoriteParkform = FavoriteParkform)
        return render_template('/Dog/NewPark.html', FavoriteParkform = FavoriteParkform)
    flash("Please fill out all fields")
    if followed is not None:
        return render_template('Dog/NewDog.html', currentUser = currentUser, CreateDogform = CreateDogform, count = count, notifications = notifications)
    else: 
        return render_template('/Dog/Initial_NewDog.html', CreateDogForm = CreateDogForm)

@app.route('/Create/Post', methods=['GET','POST'])
@login_required
def CreatePost():
    session = Database.Session()
    dogID = request.form['DogValue']
    Post = request.form['Post']
    Query = Database.tPosts(dogID=dogID, userID=current_user.id, groupID=None, Post=Post, ts=datetime.datetime.now(), image=None)
    session.add(Query)
    session.commit()
    flash('Posted successfully')
    return redirect('/dashboard')

@app.route('/Create/Finish/Dog', methods=['GET','POST'])
@login_required
def DogCreation():
    FavoriteParkform = FavoriteParkForm()
    if FavoriteParkform.validate_on_submit():
        #insert Breed
        cur, db = Tlbx.dbConnectDict()
        breedQuery = "INSERT INTO tBreed (breed) VALUES (%s);"
        data = (session.get('breed'))
        cur.execute(breedQuery, data)
        db.commit()
        breedID = cur.lastrowid

        #Insert Address then insert Favorite Park
        image = None
        addressQuery = "INSERT INTO tAddress (address, city, state, zip) VALUES (%s, %s, %s, %s);"
        data = (FavoriteParkform.address.data, FavoriteParkform.city.data, FavoriteParkform.state.data, FavoriteParkform.zipCode.data)
        cur.execute(addressQuery, data)
        favParkQuery = "INSERT INTO tFavoritePark (parkName, AddressID, image) VALUES (%s, LAST_INSERT_ID(), %s);"
        data = (FavoriteParkform.parkName.data, image)
        cur.execute(favParkQuery, data)
        db.commit()
        favParkID = cur.lastrowid

        #Insert favorite toy.
        image = None
        favToyQuery = "INSERT INTO tFavoriteToy (ToyName, image) VALUES (%s, %s);"
        data = (session['favToy'], image)
        cur.execute(favToyQuery, data)
        db.commit()
        favToyID = cur.lastrowid
        cursor = Database.Session()
        familyID = session.get('familyID')
        if familyID is None:
            familyID = cursor.query(Database.tUser.familyID).filter(Database.tUser.userID == current_user.id)
            for familyID in familyID:
                familyID = familyID.familyID

        # commit all the dog data into the database.
        dogQuery = "Insert into tDog (name, gender, breedID, fixed, age, Size, Weight, bio, image, favToyID, favParkID, familyID) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s)"
        data = (session.get('dogName'), session.get('gender'), breedID, session.get('fixed'), session.get('age'), session.get('size'), session.get('weight'), session.get('bio'), session.get('image'), favToyID, favParkID, familyID )
        cur.execute(dogQuery, data)
        db.commit()

        #Follow the dog
        sqlalch = Database.Session()
        Query = Database.tFollowers(dogID=cur.lastrowid, userID=current_user.id)
        sqlalch.add(Query)
        sqlalch.commit()
        return redirect('/dashboard')
    flash("please input your dogs favorite park")
    return render_template('/Dog/NewPark.html', FavoriteParkform = FavoriteParkform)

    #finally commit all the dog data into the database.
    dogQuery = "Insert into tDog (name, gender, breedID, fixed, age, Size, Weight, bio, image, favToyID, favParkID, familyID) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s)"
    data = (session.get('dogName'), session.get('gender'), breedID, session.get('fixed'), session.get('age'), session.get('size'), session.get('weight'), session.get('bio'), image, favToyID, favParkID, session.get('familyID') )
    cur.execute(dogQuery, data)
    db.commit()

    #Default to follow the dog
    dogID = cur.lastrowid
    FollowDogs(dogID)

    #Redirect to the dashboard
    return redirect('/dashboard')

@app.route('/User/Profile/<int:userID>', methods=['GET', 'POST'])
def userProfile(userID):
    currentUser = Tlbx.currentUserInfo(current_user.id)
    session = Database.Session()
    user = session.query(Database.tUser).filter(Database.tUser.userID == userID)
    for user in user:
        user = user

    #Get comments of posts
    commentResults = session.query(Database.tPosts.postID, Database.tComments.Comment, Database.tUser.userID, Database.tUser.firstName, Database.tUser.lastName) \
        .join(Database.tUser, Database.tComments.userID == Database.tUser.userID)\
        .join(Database.tPosts, Database.tComments.postID == Database.tPosts.postID)

    #Get reacts of posts
    reactResults = session.query(Database.tReacts.postID, Database.tUser.userID, Database.tUser.firstName, Database.tUser.lastName) \
        .join(Database.tUser, Database.tReacts.userID == Database.tUser.userID)\
        .join(Database.tPosts, Database.tReacts.postID == Database.tPosts.postID)

    #Get Posts
    postResults = session.query(Database.tPosts.postID, Database.tPosts.Post, Database.tDog.dogID, Database.tDog.name, Database.tUser.userID, Database.tUser.firstName, Database.tUser.lastName)\
    .join(Database.tFollowers, Database.tPosts.dogID == Database.tFollowers.dogID) \
    .join(Database.tUser, Database.tPosts.userID == Database.tUser.userID) \
    .join(Database.tDog, Database.tPosts.dogID == Database.tDog.dogID) \
    .filter(Database.tFollowers.userID == current_user.id).order_by(Database.tPosts.postID.desc())
    yourReacts = session.query(Database.tReacts.postID).filter(Database.tReacts.userID == userID)

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
    count, notifications = Tlbx.getNotifications(current_user.id)
    return render_template('Account/Profile.html', currentUser = currentUser, user = user, dogResults = dogResults, postResults = zip(postResults, like), commentResults = commentResults, reactResults = reactResults, count = count, notifications = notifications)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect('/')
#Run
if __name__ == "__main__":

    app.run(host='0.0.0.0', debug=True)
