import Tlbx
import Database
import datetime 

def getCountNotifications(userID):
    cur, db = Tlbx.dbConnectDict()
    query = "SELECT count(reactUser.firstName)\
    FROM tUser as reactUser \
    JOIN tReacts ON tReacts.userID = reactUser.userID \
    JOIN tPosts ON tPosts.postID = tReacts.postID \
    JOIN tUser ON tPosts.userID = tUser.userID \
    WHERE tPosts.UserID = %s \
    AND tReacts.ts > (SELECT tUser.last_message_read_time FROM tUser WHERE userID = %s) \
    UNION \
    SELECT count(commentUser.firstName) \
    FROM tUser as commentUser \
    JOIN tComments ON tComments.userID = commentUser.userID \
    JOIN tPosts ON tPosts.postID = tComments.postiD \
    JOIN tUser ON tPosts.userID = tUser.userID \
    WHERE tPosts.userID = %s \
    AND tComments.ts > (SELECT tUser.last_message_read_time FROM tUser WHERE userID = %s);"
    data = (userID, userID, userID, userID)
    cur.execute(query, data)
    counts = cur.fetchall()
    total = 0
    for count in counts:
        total = total + count['count(reactUser.firstName)']
    return total

def getNewNotifications(userID):
    cur, db = Tlbx.dbConnectDict()
    query = "SELECT count(reactUser.firstName)\
    FROM tUser as reactUser \
    JOIN tReacts ON tReacts.userID = reactUser.userID \
    JOIN tPosts ON tPosts.postID = tReacts.postID \
    JOIN tUser ON tPosts.userID = tUser.userID \
    WHERE tPosts.UserID = %s \
    AND tReacts.userID <> %s \
    AND tReacts.ts > (SELECT tUser.last_notified_time FROM tUser WHERE userID = %s) \
    UNION \
    SELECT count(commentUser.firstName) \
    FROM tUser as commentUser \
    JOIN tComments ON tComments.userID = commentUser.userID \
    JOIN tPosts ON tPosts.postID = tComments.postiD \
    JOIN tUser ON tPosts.userID = tUser.userID \
    WHERE tPosts.userID = %s \
    AND tComments.userID <> %s \
    AND tComments.ts > (SELECT tUser.last_notified_time FROM tUser WHERE userID = %s);"
    data = (userID, userID, userID, userID, userID, userID)
    cur.execute(query, data)
    counts = cur.fetchall()
    total = 0
    for count in counts:
        total = total + count['count(reactUser.firstName)']
    return total

def updateNotifyTime(userID):
    cur, db = Tlbx.dbConnectDict()
    query = "UPDATE tUser \
    SET last_notified_time = %s \
    WHERE userID = %s;"
    data = (datetime.datetime.now(), userID)
    cur.execute(query, data)

def getNotifications(userID):
    cur, db = Tlbx.dbConnectDict()
    query = "SELECT reactUser.userID, reactUser.firstName, reactUser.lastName, reactUser.image, tPosts.postID, tReacts.ts as ts, 'reacted to your post' as information\
        FROM tUser as reactUser \
        JOIN tReacts ON tReacts.userID = reactUser.userID \
        JOIN tPosts ON tPosts.postID = tReacts.postID \
        JOIN tUser ON tPosts.userID = tUser.userID \
        WHERE tPosts.UserID = %s \
        AND tReacts.userID <> %s\
        UNION \
        SELECT commentUser.userID, commentUser.firstName, commentUser.lastName, commentUser.image, tPosts.postID, tComments.ts as ts, 'commented on your post' as information \
        FROM tUser as commentUser \
        JOIN tComments ON tComments.userID = commentUser.userID \
        JOIN tPosts ON tPosts.postID = tComments.postiD \
        JOIN tUser ON tPosts.userID = tUser.userID \
        WHERE tPosts.userID = %s \
        AND tComments.userID <> %s\
        ORDER BY ts;"

    data = (userID, userID, userID, userID)
    cur.execute(query, data)
    notifications = cur.fetchall()
    count = getCountNotifications(userID)
    newNotifications = getNewNotifications(userID)
    updateNotifyTime(userID)
    return newNotifications, count, notifications
