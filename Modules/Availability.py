from Modules import Database
import datetime
def commitAvailability(dogID, userID, Begin_ts, End_ts, message):
    session = Database.Session()
    Availability = Database.tAvailability(dogID=dogID, userID = userID, Begin_ts = Begin_ts, End_ts = End_ts, message = message)
    session.add(Availability)
    session.commit()