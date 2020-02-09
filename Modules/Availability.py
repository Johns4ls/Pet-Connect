from Modules import Database
from datetime import datetime
def commitAvailability(dogID, userID, Begin_ts, End_ts, message):
    session = Database.Session()
    Availability = Database.tAvailability(dogID=dogID, userID = userID, Begin_ts = Begin_ts, End_ts = End_ts, message = message)
    session.add(Availability)
    session.commit()

def commitPlayDate(hostDogID, guestDogID, availabilityID, Begin_ts, End_ts, message):
    session = Database.Session()
    PlayDate = Database.tPlayDate(hostDogID=hostDogID, guestDogID = guestDogID, AvailabilityID = availabilityID, Begin_ts = Begin_ts, End_ts = End_ts, addressID = None)
    session.add(PlayDate)
    session.commit()
    Playdate = Database.tPosts(dogID=None, userID = None, PlayDateID = PlayDate.PlayDateID, Post = None, ts = datetime.now(), image = None)
    session.add(Playdate)
    session.commit()

def updateAvailability(availabilityID, Begin_ts, End_ts):
    session = Database.Session()
    session.query(Database.tAvailability).filter(Database.tAvailability.AvailabilityID==availabilityID)
    session.query(Database.tAvailability).filter(Database.tAvailability.AvailabilityID == availabilityID) \
        .update({Database.tAvailability.Begin_ts: Begin_ts, Database.tAvailability.End_ts: End_ts})
    session.commit()

def deleteAvailability(availabilityID):
    session = Database.Session()
    session.query(Database.tAvailability).filter(Database.tAvailability.AvailabilityID==availabilityID).delete()
    session.commit()
