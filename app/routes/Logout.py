from app import app
from Modules import Database
from flask_login import login_required, current_user, logout_user
from flask import flash, redirect
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect('/')