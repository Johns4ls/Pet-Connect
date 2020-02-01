from Modules import Comments
from flask_socketio import SocketIO, emit
from app import socketio
from flask_login import current_user
import json, ast

@socketio.on('connect', namespace='/Comments/')
def connect():
    return ''

@socketio.on('sendComment', namespace='/Comments/')
def commitComment(msg):
    try:
        msg = ast.literal_eval(json.dumps(msg))
        Comments.commitComment(current_user.id, msg)
        socketio.emit('returnComment',
                    {'message': "Success"}, namespace='/Comments/')    
    except:       
        print("bad news") 
        socketio.emit('returnComment',
                    {'message': "Fail"}, namespace='/Comments/')
@socketio.on('disconnect', namespace='/Comments/')
def disconnect():
    return ''
