#Various imports
from flask import Flask, flash, render_template, redirect
from Modules.forms import LoginForm, RegisterForm
from Modules import Tlbx
from flask_login import LoginManager, login_required, login_user, logout_user
app = Flask(__name__)

'''Secret to prevent Cross-Site Request Forgery(CSRF) attacks.
   This will need to be updated before the site goes live.'''
app.secret_key = 'some_secret'

#Flask Login Initialization
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

#Dashboard
@app.route("/Dashboard")
@login_required
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
@app.route('/', methods=['GET', 'POST'])
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
    if Registerform.validate_on_submit():
        valid = Tlbx.validate_email(Registerform.email.data)
        print(valid)
        if(Tlbx.validate_email(Registerform.email.data) is not False):
            password =  Tlbx.hash_password(Registerform.password.data)
            Tlbx.new_Account(Registerform.email.data, password)
            return redirect('/Dashboard')
        flash('Email address already exists')
        return redirect('/')
        
    return render_template('Login/login.html', Registerform=Registerform, Loginform=Loginform)
#Run
if __name__ == "__main__":

    app.run(host='0.0.0.0', debug=True)
