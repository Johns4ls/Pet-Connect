import Tlbx
import Database
import datetime 

def getLatestMessages(userID):
    cur, db = Tlbx.dbConnectDict()
    Query = ("Select tMessage.time_sent as ts, tFriend.friendID, tUser.userID, tUser.firstName, tUser.lastName, tUser.image, tMessage.message from tUser \
        JOIN tFriend ON tUser.userID = tFriend.friend \
        LEFT JOIN tMessage ON tMessage.friendID = tFriend.friendID\
        JOIN (SELECT tMessage.friendID, MAX(tMessage.time_sent) as ts FROM tMessage \
            WHERE tMessage.recipient = %s \
            GROUP by tMessage.friendID) \
            AS t2 \
            ON tMessage.friendID = t2.friendID  AND tMessage.time_sent = t2.ts\
        WHERE tFriend.user = %s \
        ORDER BY tMessage.time_sent;")
    data = (userID, userID)
    cur.execute(Query, data)
    results = cur.fetchall()
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
    Query = ("Select Count(tMessage.message) from tUser \
        JOIN tFriend ON tUser.userID = tFriend.friend \
        LEFT JOIN tMessage ON tMessage.friendID = tFriend.friendID\
        WHERE tFriend.user = %s \
        AND tMessage.recipient = %s    \
        AND tMessage.time_sent > tUser.last_message_read_time;")
    data = (userID, userID)
    cur.execute(Query, data)
    results = cur.fetchall()
    for results in results:
        results = results['Count(tMessage.message)']
    return results

def getMessages(userID):
    LatestMessages = getLatestMessages(userID)
    MessageCount = getNewMessageCount(userID, LatestMessages)
    updateMessageTime(userID)
    return LatestMessages, MessageCount

