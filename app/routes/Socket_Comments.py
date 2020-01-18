from Modules import Comments
from flask_socketio import SocketIO, emit
from app import socketio
from flask_login import current_user
@socketio.on('sendComment', namespace='/Comments/')
def commitComment(msg):
    try:
        Comments.commitComment(current_user.id, msg)
        socketio.emit('returnComment',
                    {'message': "Success"}, namespace='/Comments/')    
    except:        
        socketio.emit('returnComment',
                    {'message': "Fail"}, namespace='/Comments/')    