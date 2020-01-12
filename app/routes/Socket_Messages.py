from Modules import Tlbx, Messages
import time
from flask_socketio import SocketIO, emit
from app import socketio
from flask_login import current_user
@socketio.on('askMessages', namespace='/Messages/')
def asyncMessages(msg):
        socketio.start_background_task(SendMessages())
def SendMessages():
    Initial = True
    while(True):
        newMessages, count = Messages.getMessages(current_user.id)
        if(count != 0 and Initial is True):
            if(newMessages != 0):
                for message in newMessages:
                    message['ts'] = str(message['ts'])
                socketio.emit('getMessages',
                            {'NewMessages': newMessages, 'count': count}, namespace='/Messages/')    
            Initial = False
        time.sleep(20)