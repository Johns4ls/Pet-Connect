from Modules import Tlbx, Messages
import time
from flask_socketio import SocketIO, emit
from app import socketio
from flask_login import current_user
@socketio.on('askMessages', namespace='/Messages/')
def asyncMessages(msg):
        socketio.start_background_task(SendMessages())
def SendMessages():
    while(True):
        newMessages, count = Messages.getMessages(current_user.id)
        for message in newMessages:
            message['ts'] = str(message['ts'])
        socketio.emit('getMessages',
                    {'NewNotifications': newMessages, 'count': count}, namespace='/Messages/')    
        time.sleep(1000)