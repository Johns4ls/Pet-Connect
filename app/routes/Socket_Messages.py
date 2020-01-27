from Modules import Tlbx, Messages
import time
from flask_socketio import SocketIO, emit, disconnect
from app import socketio
from flask_login import current_user
from flask import request

@socketio.on('connect', namespace='/Messages/')
def Connect():
    return ''

@socketio.on('Messages', namespace='/Messages/')
def Messages():
    newMessages, count = Messages.getMessages(current_user.id)
    for message in newMessages:
        message['ts'] = str(message['ts'])
    socketio.emit('getMessages',
                {'NewMessages': newMessages, 'count': count}, namespace='/Messages/', room=request.sid)    
@socketio.on('disconnect', namespace='/Messages')
def disconnect():
    print('Client disconnected', request.sid)
