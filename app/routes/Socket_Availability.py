from Modules import Tlbx, Notifications, Database
import time
from flask_socketio import SocketIO, emit, test_client
from app import socketio
from flask_login import current_user
from threading import Lock
from flask import request
from Modules import Availability
import json, ast
from dateutil import parser
from pytz import timezone
@socketio.on('connect', namespace='/Availability/')
def connect():
    print("connected")
@socketio.on('getAvailability', namespace='/Availability/')
def addAvailability(msg):
    msg = ast.literal_eval(json.dumps(msg))
    eastern = timezone('US/Eastern')
    Availability.commitAvailability(msg['dogID'], msg['userID'], parser.parse(msg['Begin_ts']).astimezone(eastern), parser.parse(msg['End_ts']).astimezone(eastern), msg['message'])

@socketio.on('updateAvailability', namespace='/Availability/')
def updateAvailability(msg):
    print("doing something")
    msg = ast.literal_eval(json.dumps(msg))
    eastern = timezone('US/Eastern')
    Availability.updateAvailability(msg['availabilityID'], parser.parse(msg['Begin_ts']).astimezone(eastern), parser.parse(msg['End_ts']).astimezone(eastern))

@socketio.on('deleteAvailability', namespace='/Availability/')
def deleteAvailability(msg):
    Availability.deleteAvailability(msg['availabilityID'])


@socketio.on('askAvailability', namespace='/Availability/')
def askAvailability(dogID):
    msg = ast.literal_eval(json.dumps(dogID))
    cur, db = Tlbx.dbConnectDict()
    query = "SELECT * FROM tAvailability WHERE DogID = %s"
    data = (msg['dogID'])
    cur.execute(query, data)
    Availability = cur.fetchall()
    for time in Availability:
        time['Begin_ts'] = str(time['Begin_ts'])
        time['End_ts'] = str(time['End_ts'])
    socketio.emit('giveAvailability',
                {'Availability': Availability}, namespace='/Availability/', room=request.sid)

@socketio.on('disconnect', namespace='/Availability/')
def disconnect():
    print('Client disconnected', request.sid)