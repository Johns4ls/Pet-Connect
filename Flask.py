#Various imports
from flask import Flask, flash, render_template, redirect, session
from Modules.forms import LoginForm, RegisterForm, UserInfoForm
from Modules import Tlbx
app = Flask(__name__)

'''Secret to prevent Cross-Site Request Forgery(CSRF) attacks.
   This will need to be updated before the site goes live.'''
app.secret_key = 'some_secret'

#Initial screen upon entering website.
@app.route("/")
def index():

    #Temporary filler data
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
    return render_template('HomePage/index.html', user = user, posts = posts)

#Renders the login page
@app.route('/login', methods=['GET', 'POST'])
def login():

    #instantiates the forms to login and register your account
    Loginform = LoginForm()
    Registerform = RegisterForm()

    #Checks to ensure fields are not null
    if Loginform.validate_on_submit():
        #Checks to ensure username and password are correct.
        if(Tlbx.check_password(Loginform.email.data, Loginform.password.data) is not False):
            return redirect('/')
        flash("Email or Password is incorrect.")
    return render_template('Login/login.html', Registerform=Registerform, Loginform=Loginform)
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
        return redirect('/login')
        
    return render_template('Login/login.html', Registerform=Registerform, Loginform=Loginform)
@app.route('/userInfo', methods=['GET', 'POST'])
def userInfo():
    UserInfoform = UserInfoForm()
    firstName = UserInfoform.firstName.data
    lastName = UserInfoform.lastName.data
    email = session.get('email')
    password =  Tlbx.hash_password(session.get('password', None))
    addressNumber = UserInfoform.addressNumber.data
    stName = UserInfoform.stName.data
    city = UserInfoform.city.data
    state = UserInfoform.state.data
    zipCode = UserInfoform.zipCode.data
    Tlbx.new_Account(firstName, lastName, email, password, addressNumber, stName, city, state, zipCode)
#Run
if __name__ == "__main__":

    app.run(host='0.0.0.0', debug=True)
