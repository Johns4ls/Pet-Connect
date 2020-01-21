from Modules import Database
import datetime
from flask_login import login_required, current_user
from flask import render_template, request
from app import app
#Add a comment
@app.route('/Availability/<int:dogID>', methods=['GET', 'POST'])
def Availability(dogID):
    dogID = str(dogID)
    session = Database.Session()
    Availability = session.query(Database.tAvailability).filter(Database.tAvailability.dogID == dogID)
    return render_template('/Schedule/Availability.html', Availability = Availability)