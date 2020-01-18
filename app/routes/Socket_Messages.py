from Modules import Tlbx, Messages
import time
from flask_socketio import SocketIO, emit, disconnect
from app import socketio
from flask_login import current_user
from threading import Lock
from flask import request
messageThread = None
thread_lock = Lock()
connected = True
@socketio.on('askMessages', namespace='/Messages/')
def asyncMessages(msg):
    global initial
    initial = True
    global connected 
    connected = True
    socketio.start_background_task(SendMessages())
def SendMessages():
    initial = True
    global connected
    while(connected):
        newMessages, count = Messages.getMessages(current_user.id)
        if(count != 0 or initial is True):
            if(newMessages != 0):
                for message in newMessages:
                    message['ts'] = str(message['ts'])
                socketio.emit('getMessages',
                            {'NewMessages': newMessages, 'count': count}, namespace='/Messages/', room=request.sid)    
            initial = False
        socketio.sleep(2)
@socketio.on('disconnect', namespace='/Messages')
def test_disconnect():
    print('Client disconnected', request.sid)
    disconnect()
    global connected 
    connected = False