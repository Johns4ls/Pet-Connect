from Modules import Database
import datetime
from flask_login import login_required, current_user
from flask import render_template, request
from app import app
#Add a comment
@app.route('/Playdate/<int:dogID>', methods=['GET', 'POST'])
def Playedate(dogID):
    dogID = str(dogID)
    session = Database.Session()
    dog = session.query(Database.tDog).filter(Database.tDog.dogID == dogID)
    for dog in dog:
        dog = dog
    user = session.query(Database.tUser).filter(Database.tUser.userID == current_user.id)
    for user in user:
        user = user
    return render_template('/Playdate/Playdate.html', Availability = Availability, dog = dog, user = user)