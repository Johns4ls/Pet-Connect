from app import app
from Modules import Database, Tlbx, Messages
from flask_login import login_required, current_user
from flask import flash, redirect, render_template, request
import datetime
@app.route('/Send/Message/<int:userID>', methods=['GET','POST'])
@login_required
def sendMessage(userID):
    #user userID to get both friendIDs to submit messages

    #Get both friendIDs associated with friendship
    cur, db = Tlbx.dbConnectDict()
    query = ("SELECT friendID from tFriend \
        WHERE tFriend.user = %s \
        AND tFriend.friend = %s;")
    data = (current_user.id, userID)
    cur.execute(query, data)
    UserFriendID = cur.fetchone()
    data = (userID, current_user.id)
    cur.execute(query, data)
    FriendFriendID = cur.fetchone()
    session = Database.Session()
    message = request.form['message']

    addMessageFriend = Database.tMessage(friendID = FriendFriendID['friendID'], sender = current_user.id, \
        recipient = userID, time_Sent = datetime.datetime.now(), message = message)

    addMessageUser = Database.tMessage(friendID = UserFriendID['friendID'], sender = current_user.id, \
        recipient = userID, time_Sent = datetime.datetime.now(), message = message)


    session.add(addMessageUser)
    session.add(addMessageFriend)
    session.commit()

    return redirect('/Messages')



@app.route('/Messages', methods=['GET','POST'])
@login_required
def routeMessages():
    friendID = None
    userID = int(current_user.id)
    #Get all friends you have that you've sent messages with.
    friends, db = Tlbx.dbConnectDict()
    friendQuery = ("Select MAX(tMessage.time_sent) as ts, tFriend.friendID, tUser.userID, tUser.firstName, tUser.lastName, tUser.image from tUser \
        JOIN tFriend ON tUser.userID = tFriend.friend \
        LEFT JOIN tMessage ON tMessage.friendID = tFriend.friendID\
        WHERE tFriend.user = %s \
        GROUP BY tFriend.friendID \
        ORDER BY ts DESC;")
    data = (current_user.id)
    friends.execute(friendQuery, data)

    latestMessageQuery = (
    "Select tMessage.time_sent as ts, tFriend.friendID, tUser.userID, tUser.firstName, tUser.lastName, tMessage.message from tUser \
        JOIN tFriend ON tUser.userID = tFriend.friend \
        LEFT JOIN tMessage ON tMessage.friendID = tFriend.friendID\
        JOIN (SELECT tMessage.friendID, MAX(tMessage.time_sent) as ts FROM tMessage \
            GROUP by tMessage.friendID) \
            AS t2 \
            ON tMessage.friendID = t2.friendID  AND tMessage.time_sent = t2.ts\
        WHERE tFriend.user = %s \
        ORDER BY tMessage.time_sent DESC;")
    latest, db = Tlbx.dbConnectDict()
    data = (current_user.id)
    latest.execute(latestMessageQuery, data)

    messageQuery = ("Select tMessage.friendID, tMessage.message, tMessage.time_Sent, tMessage.recipient, tUser.firstName, tUser.lastName from tMessage \
        JOIN tFriend ON tFriend.friendID = tMessage.friendID \
        JOIN tUser ON tFriend.friend = tUser.userID \
        WHERE tFriend.user = %s \
        ORDER BY tMessage.time_sent")
    cur, db = Tlbx.dbConnectDict()
    data = (current_user.id)
    cur.execute(messageQuery, data)
    Messages.updateMessageTime(current_user.id)
    return render_template('/Messages/Messages.html', latest = latest.fetchall(), friendID = friendID, userID = userID, messages = cur.fetchall(), friends = friends.fetchall())

@app.route('/Messages/<int:friendID>', methods=['GET','POST'])
@login_required
def Message(friendID):
    userID = int(current_user.id)
    #Get all friends you have that you've sent messages with.
    friends, db = Tlbx.dbConnectDict()
    friendQuery = ("Select MAX(tMessage.time_sent) as ts, tFriend.friendID, tUser.userID, tUser.firstName, tUser.lastName, tUser.image from tUser \
        JOIN tFriend ON tUser.userID = tFriend.friend \
        LEFT JOIN tMessage ON tMessage.friendID = tFriend.friendID\
        WHERE tFriend.user = %s \
        GROUP BY tFriend.friendID \
        ORDER BY ts DESC;")
    data = (current_user.id)
    friends.execute(friendQuery, data)

    latestMessageQuery = (
    "Select tMessage.time_sent as ts, tFriend.friendID, tUser.userID, tUser.firstName, tUser.lastName, tMessage.message from tUser \
        JOIN tFriend ON tUser.userID = tFriend.friend \
        LEFT JOIN tMessage ON tMessage.friendID = tFriend.friendID\
        JOIN (SELECT tMessage.friendID, MAX(tMessage.time_sent) as ts FROM tMessage \
            GROUP by tMessage.friendID) \
            AS t2 \
            ON tMessage.friendID = t2.friendID  AND tMessage.time_sent = t2.ts\
        WHERE tFriend.user = %s \
        ORDER BY tMessage.time_sent DESC;")
    latest, db = Tlbx.dbConnectDict()
    data = (current_user.id)
    latest.execute(latestMessageQuery, data)

    messageQuery = ("Select tMessage.friendID, tMessage.message, tMessage.time_Sent, tMessage.recipient, tUser.firstName, tUser.lastName from tMessage \
        JOIN tFriend ON tFriend.friendID = tMessage.friendID \
        JOIN tUser ON tFriend.friend = tUser.userID \
        WHERE tFriend.user = %s \
        ORDER BY tMessage.time_sent")
    cur, db = Tlbx.dbConnectDict()
    data = (current_user.id)
    cur.execute(messageQuery, data)
    Messages.updateMessageTime(current_user.id)
    return render_template('/Messages/Messages.html', friendID = friendID, userID = userID, latest = latest.fetchall(), messages = cur.fetchall(), friends = friends.fetchall())