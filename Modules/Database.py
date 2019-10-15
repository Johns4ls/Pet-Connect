from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import create_engine
import sqlalchemy
import pymysql
engine = sqlalchemy.create_engine(
    'mysql+pymysql://Website:W3bsite!@localhost:3306/PetConnect',
    echo=True)
 
# Define and create all tables in the DB
Base = declarative_base()
class tUser(Base):
    __tablename__ = 'tUser'
    userID = Column(Integer, primary_key=True)
    firstName = Column('firstName', String(255))
    lastName = Column('lastName', String(255))
    email = Column('email', String(255))
    familyID = Column(Integer, ForeignKey('tFamily.familyID'))
    password = Column('password', String(255))
    image = Column('image', String(255))
    addressID = Column(Integer, ForeignKey('tAddress.addressID'))

class tAddress(Base):
    __tablename__ = 'tAddress'
    addressID = Column(Integer, primary_key=True)
    address = Column('address', String(255))
    city = Column('city', String(255))
    state = Column('state', String(255))
    zip = Column('zip', Integer)

class tDog(Base):
    __tablename__ = 'tDog'
    dogID = Column(Integer, primary_key=True)
    name = Column('name', String(255))
    gender = Column('gender', Integer)
    breedID = Column(Integer, ForeignKey('tBreed.breedID'))
    fixed = Column('fixed', String(255))
    age = Column('age', Integer)
    Size = Column('Size', String(255))
    weight = Column('weight', Integer)
    bio = Column('bio', String(255))
    image = Column('image', String(255))
    favToyID = Column(Integer, ForeignKey('tFavoriteToy.favToyID'))
    favParkID = Column(Integer, ForeignKey('tFavoritePark.favParkID'))
    familyID = Column(Integer, ForeignKey('tFamily.familyID'))

class tBreed(Base):
    __tablename__ = 'tBreed'
    breedID = Column(Integer, primary_key=True)
    breed = Column('breed', String(255))

class tFamily(Base):
    __tablename__ = 'tFamily'
    familyID = Column(Integer, primary_key=True)
    familyName = Column('breed', String(255))
    headofHouseID = Column(Integer, ForeignKey('tHeadofHouse.headofHouseID'))

class tAdmin(Base):
    __tablename__ = 'tAdmin'
    adminID = Column(Integer, primary_key=True)
    dogID = Column(Integer, ForeignKey('tDog.dogID'))
    userID = Column(Integer, ForeignKey('tUser.userID'))

class tFavoriteToy(Base):
    __tablename__ = 'tFavoriteToy'
    favToyID = Column(Integer, primary_key=True)
    ToyName = Column('ToyName', String(255))
    image = Column('image', String(255))

class tFavoritePark(Base):
    __tablename__ = 'tFavoritePark'
    favParkID = Column(Integer, primary_key=True)
    parkName = Column('ToyName', String(255))
    addressID = Column(Integer, ForeignKey('tAddress.addressID'))
    image = Column('image', String(255))

class tfollowers(Base):
    __tablename__ = 'tFollowers'
    followID = Column(Integer, primary_key=True)
    dogID = Column(Integer, ForeignKey('tDog.dogID'))
    userID = Column(Integer, ForeignKey('tUser.userID'))

class tPosts(Base):
    __tablename__ = 'tPosts'
    postID = Column(Integer, primary_key=True)
    dogID = Column(Integer, ForeignKey('tDog.dogID'))
    userID = Column(Integer, ForeignKey('tUser.userID'))
    groupID = Column(Integer, ForeignKey('tGroup.groupID'))
    Post = Column('Post', String(255))
    ts = Column('ts', DateTime)
    image = Column('image', String(255))

class tPostPictures(Base):
    __tablename__ = 'tPostPictures'
    postPictureID = Column(Integer, primary_key=True)
    image = Column('image', String(255))
    postID = Column(Integer, ForeignKey('tPost.postID'))

class tComments(Base):
    __tablename__ = 'tComments'
    commentID = Column(Integer, primary_key=True)
    postID = Column(Integer, ForeignKey('tPosts.postID'))
    dogID = Column(Integer, ForeignKey('tDog.dogID'))
    userID = Column(Integer, ForeignKey('tUser.userID'))
    Post = Column('Post', String(255))
    ts = Column('ts', DateTime)
    image = Column('image', String(255))


class tReacts(Base):
    __tablename__ = 'tReacts'
    reactID = Column(Integer, primary_key=True)
    reactTypeID = Column(Integer, ForeignKey('tReactType.reactTypeID'))
    postID = Column(Integer, ForeignKey('tPosts.postID'))

class tReactTypes(Base):
    __tablename__ = 'tReactTypes'
    reactTypeID = Column(Integer, primary_key=True)
    reactType = Column('reactType', String(255))

class tAvailability(Base):
    __tablename__ = 'tAvailability'
    AvailabilityID = Column(Integer, primary_key=True)
    dogID = Column(Integer, ForeignKey('tDog.dogID'))
    userID = Column(Integer, ForeignKey('tUser.userID'))
    Begin_ts = Column('Begin_ts', DateTime)
    End_ts = Column('End_ts', DateTime)

class tPlayDateTime(Base):
    __tablename__ = 'tPlayDateTime'
    playdateTimeID = Column(Integer, primary_key=True)
    playDateID = Column(Integer, ForeignKey('tPlayDate.playDateID'))
    Begin_ts = Column('Begin_ts', DateTime)
    End_ts = Column('End_ts', DateTime)
    addressID = Column(Integer, ForeignKey('tAddress.addressID'))

class tPlayDate(Base):
    __tablename__ = 'tPlayDate'
    playdateID = Column(Integer, primary_key=True)
    dogID = Column(Integer, ForeignKey('tDog.dogID'))
    userID = Column(Integer, ForeignKey('tUser.userID'))

class tMessage(Base):
    __tablename__ = 'tMessage'
    messageID = Column(Integer, primary_key=True)
    userTo_ID = Column(Integer, ForeignKey('tUser.userID'))
    userFrom_ID = Column(Integer, ForeignKey('tUser.userID'))
    ts = Column('ts', DateTime)

class tPictureMessage(Base):
    __tablename__ = 'tPictureMessage'
    pictureMessageID = Column(Integer, primary_key=True)
    image = Column('image', String(255))
    message_ID = Column(Integer, ForeignKey('tMessage.messageID'))


class tInterests(Base):
    __tablename__ = 'tInterests'
    interestsID = Column(Integer, primary_key=True)
    Interests = Column('Interests', String(255))
    Disinterests = Column('Disinterests', String(255))

class tDogInterests(Base):
    __tablename__ = 'tDogInterests'
    DogInterestsID = Column(Integer, primary_key=True)
    interestsID = Column(Integer, ForeignKey('tInterests.interestsID'))
    dogID = Column(Integer, ForeignKey('tDog.dogID'))

class tGroupParticipants(Base):
    __tablename__ = 'tGroupParticipants'
    GroupParticipantsID = Column(Integer, primary_key=True)
    userID = Column(Integer, ForeignKey('tUser.userID'))
    groupID = Column(Integer, ForeignKey('tGroup.groupID'))

class tGroup(Base):
    __tablename__ = 'tGroup'
    groupID = Column(Integer, primary_key=True)
    Name = Column('Name', String(255))
    image = Column('image', String(255))

class tHeadofHouse(Base):
    __tablename__ = 'tHeadofHouse'
    headofHouseID = Column(Integer, primary_key=True)
    userID = Column(Integer, ForeignKey('tUser.userID'))

 
Base.metadata.create_all(engine)

def Session():
    # Create a session
    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    return session

''' Example queries 
# Add a user
jwk_user = tUser(firstName='jesper', lastName='Krogh', email='jkrogh@gmail.com', password='spoopy', image = '')
session.add(jwk_user)
session.commit()
 
# Query the user
our_user = session.query(tUser).filter_by(firstName='jesper').first()
print('\nOur User:')
print(our_user)

session.query(tUser.firstName, '_score') \
.filter(match(Character.quote_ft, 'space')) \
.all()


'''