from Modules import Tlbx, Notifications
import time
from flask_socketio import SocketIO, emit, disconnect, test_client
from app import socketio
from flask_login import current_user
from threading import Lock
from flask import request
from Modules import Availability
@socketio.on('connect', namespace='/Availability/')
def connect():
    print("connected")
@socketio.on('getAvailability', namespace='/Availability/')
def addAvailability(msg):
    Availability.commitAvailability(msg.dogID, msg.userID, msg.Begin_ts, msg.End_ts, msg.message)
    print(msg)
@socketio.on('disconnect', namespace='/Availability/')
def disconnect():
    print('Client disconnected', request.sid)