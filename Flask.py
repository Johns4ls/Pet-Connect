#Various imports
from flask import Flask, flash, render_template, redirect, session
from Modules.forms import LoginForm, RegisterForm, UserInfoForm
from Modules import Tlbx
from flask_login import LoginManager, login_required, logout_user
app = Flask(__name__)

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

    '''Will be here soon! Need to add the 
    ability to create new posts on the Dashboard
    once dogs are made, since Users are now
    able to hit the Dashboard. This will require
    JavaScript to submit the request without redirecting.
    The posts submits will be there own separate route.
    Much like likes will.'''
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
    return render_template('HomePage/Dashboard.html', user = user, posts = posts)

#Renders the login page
@app.route('/', methods=['GET', 'POST'])
def login():

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
@app.route('/userInfo', methods=['GET', 'POST'])
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
    return redirect('/dashboard')

@app.route('/forgotPass', methods=['GET', 'POST'])
def forgotPass():
    return render_template('PasswordReset/PasswordReset.html')

@app.route('/PasswordReset', methods=['GET','POST'])
def passwordReset():
    print("WIP")

@app.route('/FamilyCreation', methods=['GET','POST'])
@login_required
def familyCreation():
    print("Create a new Family.")

@app.route('/JoinFamily', methods=['GET','POST'])
@login_required
def JoinFamily():
    print("Join an Existing family.")

@app.route('/DogCreation', methods=['GET','POST'])
@login_required
def DogCreation():
    '''We may want to split these into functions...
    If we let users have the ability to update these items
    it may be easier to just call a function from tlbx.'''
    #Query for breed existence in DB here
    if (breedID is None)
        cur, db = dbConnectDict()
        breedQuery = "INSERT INTO tbreed (breed) VALUES (%s);"
        data = (breed)
        cur.execute(breedQuery, data)
        db.commit()
        breedID = cur.insert_id()
    #Query for favorite park existence in DB here
    if (favParkID is None)
        image = None
        addressQuery = "INSERT INTO tAddress (address, city, state, zip) VALUES (%s, %s, %s, %s);"
        data = (address, city, state zipCode)
        cur.execute(addressQuery, data)
        favParkQuery = "INSERT INTO tFavoritePark (parkName, AddressID, image) VALUES (%s, LAST_INSERT_ID(), %s);"
        data = (parkName, image)
        cur.execute(favParkQuery, data)
        db.commit()
        favParkID = cur.insert_id()
    #Wuery for favorite toy here... Combo box?
    if (favToyID is None)
        image = None
        favToyQuery = "INSERT INTO tFavoriteToy (ToyName, image) VALUES (%s, %s);"
        data = (ToyName, image)
        cur.execute(favToyQuery, data)
        db.commit()
        favToyID = cur.insert_id()

#finally commit all the dog data into the database.
dogQuery = "Insert into tDog (breedID, gender, fixed, age, favParkID, favToyID, Size, Weight, bio, image"
data = (breedID, gender, fixed, age, favParkID, favToyID, Size, weight, bio, image)
cur.execute(dogQuery, data)
db.commit()

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect('/')
#Run
if __name__ == "__main__":

    app.run(host='0.0.0.0', debug=True)
