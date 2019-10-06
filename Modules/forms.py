from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, EqualTo
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    passwordConfirm = PasswordField('passwordConfirm', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
class UserInfoForm(FlaskForm):
    firstName = StringField('firstName', validators=[DataRequired()])
    lastName = StringField('lastName', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = StringField('state', validators=[DataRequired()])
    zipCode = StringField('zipCode', validators=[DataRequired()])
    submit = SubmitField('Register')
class CreateFamilyForm(FlaskForm):
    surName = StringField('surName', validators=[DataRequired()])
    submit = SubmitField('Create Family')
class CreateDogForm(FlaskForm):
    Genders=[('Male', 'Male'), ('Female', 'Female')] 
    Fixed = [('Yes','Yes,'), ('No', 'No')]
    Sizes = [('Extra Small','Extra Small'), ('Small','Small'), ('Medium','Medium'), ('Large', 'Large'), ('Very large', 'Very large')]
    dogName = StringField('name', validators=[DataRequired()])
    gender = SelectField('gender', choices = Genders, validators = [DataRequired()])
    breed = StringField('breed', validators=[DataRequired()])
    fixed = SelectField('fixed', choices = Fixed, validators = [DataRequired()])
    age = StringField('age', validators=[DataRequired()])   
    favToy = StringField('favToy', validators=[DataRequired()]) 
    size = SelectField('fixed', choices = Sizes, validators = [DataRequired()])
    weight = StringField('weight', validators=[DataRequired()]) 
    bio = StringField('bio') 
    submit = SubmitField('Next')
class FavoriteParkForm(FlaskForm):
    parkName = StringField('surName', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = StringField('state', validators=[DataRequired()])
    zipCode = StringField('zipCode', validators=[DataRequired()])
    submit = SubmitField('Register')