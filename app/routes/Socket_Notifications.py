from Modules import Tlbx, Notifications
import time
from flask_socketio import SocketIO, emit, disconnect, test_client
from app import socketio
from flask_login import current_user
from flask import request

@socketio.on('connect', namespace='/Notifications/')
def test_connect():
    return ''

@socketio.on('askNotifications', namespace='/Notifications/')
def send():
    NewNotifications, count, notifications = Notifications.getNotifications(current_user.id)
    for notification in notifications:
        notification['ts'] = str(notification['ts'])
    emit('getNotifications',
                {'NewNotifications': NewNotifications, 'count': count, 'notifications': notifications}, namespace='/Notifications/')

@socketio.on('disconnect', namespace='/Notifications/')
def test_disconnect():
    print('Client disconnected', request.sid)
