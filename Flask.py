#Various imports
from flask import Flask, flash, render_template, redirect, session, request
from Modules.forms import LoginForm, RegisterForm, UserInfoForm, CreateFamilyForm, CreateDogForm, FavoriteParkForm
from Modules import Tlbx, Database
from flask_sqlalchemy import SQLAlchemy, functools
from flask_login import LoginManager, login_required, logout_user, current_user
app = Flask(__name__)
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
    session = Database.Session()
    results = session.query(Database.tDog.name).join(Database.tUser, Database.tDog.familyID == Database.tUser.familyID).filter(Database.tUser.userID == current_user.id)
    user = {'username': 'Larry'}
    posts = [
    {
        'author': {'username': 'John'},
        'body': 'Beautiful day in Portland!'
    },
    {
        'author': {'username': 'Susan'},
        'body': 'The Avengers movie was so cool!'
    }
]
    return render_template('HomePage/Dashboard.html', user = user, posts = posts, results = results)

@app.route('/Create/Post', methods=['GET','POST'])
@login_required
def CreateNewPost():
    CreateFamilyform = CreateFamilyForm()

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
    firstName = UserInfoform.firstName.data
    lastName = UserInfoform.lastName.data
    email = session.get('email')
    password =  Tlbx.hash_password(session.get('password', None))
    address = UserInfoform.address.data
    city = UserInfoform.city.data
    state = UserInfoform.state.data
    zipCode = UserInfoform.zipCode.data
    Tlbx.new_Account(firstName, lastName, email, password, address, city, state, zipCode)
    Tlbx.loginUser(email)
    return render_template('/Family/FamilySplash.html')

@app.route('/forgotPass', methods=['GET', 'POST'])
def forgotPass():
    return render_template('PasswordReset/PasswordReset.html')

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
    CreateFamilyform = CreateFamilyForm()
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


@app.route('/Join/Family', methods=['GET','POST'])
@login_required
def JoinFamily():
    return render_template('/Family/JoinFamily.html')
   
@app.route('/follow/<int:dogID>', methods=['GET','POST'])
@login_required
def FollowDogs(dogID):
   session = Database.Session()
   addFollower = Database.tfollowers(dogID = dogID, userID= current_user.id)
   session.add(addFollower)
   session.commit()
   return '', 204

@app.route('/Search', methods=['GET','POST'])
@login_required
def Search():
    #Do we want to do a like to prevent ALL dogs from being searched and sorted by relevance?
    session = Database.Session()
    Name = request.form['Search']
    dogs = session.query(Database.tDog).filter(Database.tDog.name.contains(Name) | (Database.tDog.name.op('SOUNDS LIKE')(Name))).order_by(Database.tDog.name.match(Name).desc()).all()

    return render_template('/Search/Search.html', results = dogs)

@app.route('/Create/New/Dog', methods=['GET','POST'])
@login_required
def CreateNewDog():
    CreateDogform = CreateDogForm()
    return render_template('Dog/NewDog.html', CreateDogform = CreateDogform)

@app.route('/Create/Start/Park', methods=['GET','POST'])
@login_required
def StartPark():
    CreateDogform = CreateDogForm()
    session['dogName'] = CreateDogform.dogName.data
    session['gender'] = CreateDogform.gender.data
    session['breed'] = CreateDogform.breed.data
    session['fixed'] = CreateDogform.fixed.data
    session['age'] = CreateDogform.age.data
    session['favToy'] = CreateDogform.favToy.data
    session['size'] = CreateDogform.size.data
    session['weight'] = CreateDogform.weight.data
    session['bio'] = CreateDogform.bio.data  
    FavoriteParkform = FavoriteParkForm()
    return render_template('/Dog/NewPark.html', FavoriteParkform = FavoriteParkform)

@app.route('/Create/Finish/Dog', methods=['GET','POST'])
@login_required
def DogCreation():
    #insert Breed
    cur, db = Tlbx.dbConnectDict()
    breedQuery = "INSERT INTO tBreed (breed) VALUES (%s);"
    data = (session.get('breed'))
    cur.execute(breedQuery, data)
    db.commit()
    breedID = cur.lastrowid

    #Insert Address then insert Favorite Park
    FavoriteParkform = FavoriteParkForm()
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
    data = (session.get('dogName'), session.get('gender'), breedID, session.get('fixed'), session.get('age'), session.get('size'), session.get('weight'), session.get('bio'), image, favToyID, favParkID, session.get('familyID') )
    cur.execute(dogQuery, data)
    db.commit()
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
