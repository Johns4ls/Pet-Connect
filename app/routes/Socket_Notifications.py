from Modules import Tlbx, Notifications
import time
from flask_socketio import SocketIO, emit, disconnect, test_client
from app import socketio
from flask_login import current_user
from flask import request

@socketio.on('connect', namespace='/Notifications/')
def connect():
    return ''

@socketio.on('Notifications', namespace='/Notifications/')
def asyncNotifications():
    NewNotifications, count, notifications = Notifications.getNotifications(current_user.id)
        for notification in notifications:
            notification['ts'] = str(notification['ts'])
        socketio.emit('getNotifications',
                    {'NewNotifications': NewNotifications, 'count': count, 'notifications': notifications}, namespace='/Notifications/', room=request.sid)

@socketio.on('disconnect', namespace='/Notifications/')
def disconnect():
    print('Client disconnected', request.sid)
