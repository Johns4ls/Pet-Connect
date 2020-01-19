from Modules import Tlbx, Notifications
import time
from flask_socketio import SocketIO, emit, disconnect, test_client
from app import socketio
from flask_login import current_user
from threading import Lock
from flask import request
notifyThread = None
connected = True
@socketio.on('askNotifications', namespace='/Notifications/')
def asyncNotifications(msg):
    global initial
    initial = True
    global connected 
    connected = True
    socketio.start_background_task(SendNotifications())
def SendNotifications():
    initial = True
    global connected 
    while(connected):
        NewNotifications, count, notifications = Notifications.getNotifications(current_user.id)
        if(count != 0 or initial is True):
            for notification in notifications:
                notification['ts'] = str(notification['ts'])
            socketio.emit('getNotifications',
                        {'NewNotifications': NewNotifications, 'count': count, 'notifications': notifications}, namespace='/Notifications/', room=request.sid) 
            initial = False
        socketio.sleep(2)
@socketio.on('disconnect', namespace='/Notifications/')
def test_disconnect():
    print('Client disconnected', request.sid)
    disconnect()
    global connected 
    connected = False