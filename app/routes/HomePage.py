from Modules import Tlbx
from Modules.forms import LoginForm, RegisterForm, UserInfoForm
from flask import Flask, flash, render_template, redirect, session, request
from flask_login import login_required, current_user
from app import app
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
    return render_template('/Login/login.html', Registerform=Registerform, Loginform=Loginform)

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