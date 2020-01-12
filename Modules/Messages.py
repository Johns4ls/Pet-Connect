import Tlbx
import Database
import datetime 

def getLatestMessages(userID):
    cur, db = Tlbx.dbConnectDict()
    Query = ("Select tMessage.message, MAX(tMessage.time_sent) as ts, tFriend.friendID, tUser.userID, tUser.firstName, tUser.lastName, tUser.image from tUser \
        JOIN tFriend ON tUser.userID = tFriend.friend \
        LEFT JOIN tMessage ON tMessage.friendID = tFriend.friendID\
        WHERE tFriend.user = %s \
        GROUP BY tFriend.friendID \
        ORDER BY ts DESC;")
    data = (userID)
    results = cur.execute(Query, data)
    return results

def updateMessageTime(userID):
    cur, db = Tlbx.dbConnectDict()
    query = "UPDATE tUser \
    SET last_message_read_time = %s \
    WHERE userID = %s;"
    data = (datetime.datetime.now(), userID)
    cur.execute(query, data)

def getNewMessageCount(userID, LatestMessages):
    cur, db = Tlbx.dbConnectDict()
    Query = ("Select Count(tMessage.message), MAX(tMessage.time_sent) as ts, tFriend.friendID, tUser.userID, \
        tUser.firstName, tUser.lastName, tUser.image, tUser.last_message_read_time from tUser \
        JOIN tFriend ON tUser.userID = tFriend.friend \
        LEFT JOIN tMessage ON tMessage.friendID = tFriend.friendID\
        WHERE tFriend.user = %s \
        AND ts > tUser.last_message_read_time\
        GROUP BY tFriend.friendID;")
    data = (userID)
    results = cur.execute(Query, data)
    return results

def getMessages(userID):
    LatestMessages = getLatestMessages(userID)
    NotificationCount = getNewMessageCount(userID, LatestMessages)
    updateMessageTime(userID)
    return LatestMessages, NotificationCount

