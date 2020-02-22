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

@socketio.on('getPlayDate', namespace='/Availability/')
def addPlaydate(msg):
    msg = ast.literal_eval(json.dumps(msg))
    eastern = timezone('US/Eastern')
    cur, db = Tlbx.dbConnectDict()
    query = "SELECT * FROM tPlayDate WHERE AvailabilityID = %s"
    data = (msg['AvailabilityID'])
    cur.execute(query, data)
    playdate = cur.fetchall()
    if (playdate != ()):
        socketio.emit('PlayDateException',
        {'Error': "This time is in use by another playdate."}, namespace='/Availability/', room=request.sid)
    else:
        Availability.commitPlayDate(msg['hostDogID'], msg['guestDogID'], msg['creatorID'] ,msg['AvailabilityID'], parser.parse(msg['Begin_ts']).astimezone(eastern), parser.parse(msg['End_ts']).astimezone(eastern), msg['message'])
@socketio.on('updateAvailability', namespace='/Availability/')
def updateAvailability(msg):
    msg = ast.literal_eval(json.dumps(msg))
    eastern = timezone('US/Eastern')
    try:
        Availability.updateAvailability(msg['AvailabilityID'], parser.parse(msg['Begin_ts']).astimezone(eastern), parser.parse(msg['End_ts']).astimezone(eastern))
        socketio.emit('AvailabilitySuccess',
                {'Success': 'Success'}, namespace='/Availability/', room=request.sid)
    except:
        socketio.emit('AvailabilityException',
                {'Error': "You cannot update availability if it is in use for a playdate."}, namespace='/Availability/', room=request.sid)

@socketio.on('deleteAvailability', namespace='/Availability/')
def deleteAvailability(msg):
    try:
        print(msg['AvailabilityID'])
        Availability.deleteAvailability(msg['AvailabilityID'])
        socketio.emit('AvailabilitySuccess',
                {'Success': 'Success'}, namespace='/Availability/', room=request.sid)
    except:
        socketio.emit('AvailabilityException',
                {'Error': "You cannot delete availability if it is in use for a playdate."}, namespace='/Availability/', room=request.sid)

@socketio.on('deletePlayDate', namespace='/Availability/')
def deletePlayDate(msg):
    try:
        Availability.deletePlayDate(msg['PlayDateID'])
        socketio.emit('PlayDateDeleteSuccess',
                {'Success': 'Success'}, namespace='/Availability/', room=request.sid)
    except:
        socketio.emit('PlayDateException',
                {'Error': "There was an error deleting the playdate."}, namespace='/Availability/', room=request.sid)



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

@socketio.on('askPlayDates', namespace='/Availability/')
def askPlayDate(dogID):
    msg = ast.literal_eval(json.dumps(dogID))
    cur, db = Tlbx.dbConnectDict()
    query = "SELECT *, hostDog.name, guestDog.name FROM tPlayDate \
        JOIN tDog hostDog ON tPlayDate.hostDogID = hostDog.dogID \
        JOIN tDog guestDog ON tPlayDate.guestDogID = guestDog.dogID \
        WHERE tPlayDate.hostDogID = %s"
    data = (msg['dogID'])
    cur.execute(query, data)
    Availability = cur.fetchall()
    for time in Availability:
        time['Begin_ts'] = str(time['Begin_ts'])
        time['End_ts'] = str(time['End_ts'])
    socketio.emit('givePlayDates',
                {'PlayDates': Availability}, namespace='/Availability/', room=request.sid)

@socketio.on('disconnect', namespace='/Availability/')
def disconnect():
    print('Client disconnected', request.sid)