from Modules import Tlbx, Notifications
import time
from flask_socketio import SocketIO, emit
from app import socketio
from flask_login import current_user
@socketio.on('askNotifications', namespace='/Notifications/')
def asyncNotifications(msg):
        socketio.start_background_task(SendNotifications())
def SendNotifications():
    while(True):
        NewNotifications, count, notifications = Notifications.getNotifications(current_user.id)
        for notification in notifications:
            notification['ts'] = str(notification['ts'])
        socketio.emit('getNotifications',
                    {'NewNotifications': NewNotifications, 'count': count, 'notifications': notifications}, namespace='/Notifications/')    
        time.sleep(1000)