#Various imports
from flask import Flask, flash, render_template, redirect, session, request
from werkzeug.utils import secure_filename
from Modules.forms import LoginForm, RegisterForm, UserInfoForm, CreateFamilyForm, CreateDogForm, FavoriteParkForm, PasswordResetForm
from Modules import Tlbx, Database
from flask_sqlalchemy import SQLAlchemy, functools
from sqlalchemy import and_
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
    user = session.query(Database.tUser).filter(Database.tUser.userID == current_user.id)
    for user in user:
        user = user
    #Collect dogs in your family
    dogResults = session.query(Database.tDog).join(Database.tUser, Database.tDog.familyID == Database.tUser.familyID).filter(Database.tUser.userID == current_user.id)

    #Get comments of posts
    commentResults = session.query(Database.tPosts.postID, Database.tComments.Comment, Database.tUser.firstName, Database.tUser.lastName) \
        .join(Database.tUser, Database.tComments.userID == Database.tUser.userID)\
        .join(Database.tPosts, Database.tComments.postID == Database.tPosts.postID)

    #Get reacts of posts
    reactResults = session.query(Database.tReacts.postID, Database.tUser.firstName, Database.tUser.lastName) \
        .join(Database.tUser, Database.tReacts.userID == Database.tUser.userID)\
        .join(Database.tPosts, Database.tReacts.postID == Database.tPosts.postID)

    #Get Posts
    postResults = session.query(Database.tPosts.postID, Database.tPosts.Post, Database.tDog.name, Database.tUser.firstName, Database.tUser.lastName)\
    .join(Database.tFollowers, Database.tPosts.dogID == Database.tFollowers.dogID) \
    .join(Database.tUser, Database.tPosts.userID == Database.tUser.userID) \
    .join(Database.tDog, Database.tPosts.dogID == Database.tDog.dogID) \
    .filter(Database.tFollowers.userID == current_user.id)

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


    return render_template('HomePage/Dashboard.html', user = user, dogResults = dogResults, postResults = zip(postResults, like), commentResults = commentResults, reactResults = reactResults)

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
    Like = Database.tReacts(userID=current_user.id, postID=postID)
    session.add(Like)
    session.commit()
    return '', 204

#Remove a like
@app.route('/Unlike/<int:postID>', methods=['GET', 'POST'])
def Unlike(postID):
    postID=str(postID)
    session = Database.Session()
    session.query(Database.tReacts).filter(Database.tReacts.reactID==postID) \
    .filter(Database.tReacts.userID==current_user.id).delete()
    session.commit()
    return '', 204

#Add a comment
@app.route('/Create/Comment/<int:postID>', methods=['GET', 'POST'])
def Comment(postID):
    postID = str(postID)
    Comment = request.form['Comment']
    session = Database.Session()
    Comment = Database.tComments(postID=postID, userID = current_user.id, Comment = Comment, ts=datetime.datetime.now(), image=None)
    session.add(Comment)
    session.commit()
    return '', 204

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
    sqlalch.commit()
    CreateFamilyform = CreateFamilyForm()
    if CreateFamilyform.validate_on_submit():
        CreateDogform = CreateDogForm()
        familyName = CreateFamilyform.surName.data
        cur, db = Tlbx.dbConnectDict()
        cursor= Database.Session()
        query = ("INSERT INTO tFamily (familyName, headofHouseID) VALUES(%s, %s);")
        data = (familyName, current_user.id)
        cur.execute(query, data)
        session['familyID'] = db.insert_id()
        x = cursor.query(Database.tUser).get(current_user.id)
        x.familyID = db.insert_id()
        cursor.commit()
        return render_template('Dog/NewDog.html', CreateDogform = CreateDogform)
    flash("Please add a family name")
    return render_template('/Family/FamilyCreate.html', CreateFamilyform = CreateFamilyform )


@app.route('/Join/Family', methods=['GET','POST'])
@login_required
def JoinFamily():
    return render_template('/Family/JoinFamily.html')

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

@app.route('/Search', methods=['GET','POST'])
@login_required
def Search():
    session = Database.Session()
    Name = request.form['Search']
    dogs = session.query(Database.tDog).filter(Database.tDog.name.contains(Name) | (Database.tDog.name.op('SOUNDS LIKE')(Name))).order_by(Database.tDog.name.match(Name).desc()).all()
    followed = session.query(Database.tFollowers).filter(Database.tFollowers.userID == current_user.id)
    texts={}
    text =[]
    for dog in dogs:
        texts[dog.dogID] = 'Follow'
    for follower in followed:
        if follower.dogID in texts.keys():
            texts[follower.dogID] = 'Unfollow'         
    for dog in dogs:
        text.append(texts[dog.dogID])
    return render_template('/Search/Search.html', results = zip(dogs, text))

@app.route('/Create/New/Dog', methods=['GET','POST'])
@login_required
def CreateNewDog():
    CreateDogform = CreateDogForm()
    return render_template('Dog/NewDog.html', CreateDogform = CreateDogform)

@app.route('/Create/Start/Park', methods=['GET','POST'])
@login_required
def StartPark():
    CreateDogform = CreateDogForm()
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
        return render_template('/Dog/NewPark.html', FavoriteParkform = FavoriteParkform)
    flash("Please fill out all fields")
    return render_template('Dog/NewDog.html', CreateDogform = CreateDogform)

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
    session = Database.Session()
    user = session.query(Database.tUser).filter(Database.tUser.userID == current_user.id)
    for user in user:
        user = user
    #Collect dogs in your family
    dogResults = session.query(Database.tDog).join(Database.tUser, Database.tDog.familyID == Database.tUser.familyID).filter(Database.tUser.userID == current_user.id)

    #Get comments of posts
    commentResults = session.query(Database.tPosts.postID, Database.tComments.Comment, Database.tUser.firstName, Database.tUser.lastName) \
        .join(Database.tUser, Database.tComments.userID == Database.tUser.userID)\
        .join(Database.tPosts, Database.tComments.postID == Database.tPosts.postID)

    #Get reacts of posts
    reactResults = session.query(Database.tReacts.postID, Database.tUser.firstName, Database.tUser.lastName) \
        .join(Database.tUser, Database.tReacts.userID == Database.tUser.userID)\
        .join(Database.tPosts, Database.tReacts.postID == Database.tPosts.postID)

    #Get Posts
    postResults = session.query(Database.tPosts.postID, Database.tPosts.Post, Database.tDog.name, Database.tUser.firstName, Database.tUser.lastName)\
    .join(Database.tFollowers, Database.tPosts.dogID == Database.tFollowers.dogID) \
    .join(Database.tUser, Database.tPosts.userID == Database.tUser.userID) \
    .join(Database.tDog, Database.tPosts.dogID == Database.tDog.dogID) \
    .filter(Database.tFollowers.userID == current_user.id)

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


    return render_template('HomePage/Dashboard.html', user = user, dogResults = dogResults, postResults = zip(postResults, like), commentResults = commentResults, reactResults = reactResults)

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

        #finally commit all the dog data into the database.
        dogQuery = "Insert into tDog (name, gender, breedID, fixed, age, Size, Weight, bio, image, favToyID, favParkID, familyID) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s)"
        data = (session.get('dogName'), session.get('gender'), breedID, session.get('fixed'), session.get('age'), session.get('size'), session.get('weight'), session.get('bio'), session.get('image'), favToyID, favParkID, session.get('familyID') )
        cur.execute(dogQuery, data)
        db.commit()
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

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect('/')
#Run
if __name__ == "__main__":

    app.run(host='0.0.0.0', debug=True)
