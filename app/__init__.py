from flask import Flask
from flask_login import LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy, functools
from flask_socketio import SocketIO, emit
from Modules import Tlbx
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
async_mode = None
socketio = SocketIO(app, async_mode=async_mode)
login_manager.login_view = "/"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
'''Secret to prevent Cross-Site Request Forgery(CSRF) attacks.
   This will need to be updated before the site goes live.'''
app.secret_key = 'some_secret'
from routes import Availability, Comments, CreateDog, Dashboard, Follow, Friend, HomePage, Likes, Logout, Messages
from routes import NewAccount, Socket_Notifications, Password, Posts, Profile, Search, Socket_Messages, Socket_Availability, Socket_Comments, Playdate
@login_manager.user_loader
def load_user(userid):
    return Tlbx.userRefresh(userid)
