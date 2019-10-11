from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

engine = sqlalchemy.create_engine(
    'mysql+mysqlconnector://Website:W3bsite!@localhost:3306/PetConnect',
    echo=True)
 
# Define and create the table
Base = declarative_base()
class tUser(Base):
    __tablename__ = 'tUser'
    userID = Column('userID', Integer, primary_key=True)
    firstName = Column('firstName', String(255))
    lastName = Column('lastName', String(255))
    email = Column('email', String(255))
    password = Column('password', String(255))
    image = Column('image', String(255))
    adressID = Column('addressID', Integer, ForeignKey('tAddress.addressID'))
    familyID = Column('familyID', Integer, ForeignKey('tFamily.familyID'))

class tAddress(Base):
    __tablename__ = 'tAddress'
    addressID = Column('addressID', Integer, primary_key=True)
    Column('address', String(255))
    Column('city', String(255))
    Column('state', String(255))
    Column('zip', Integer)

class tFamily(Base):
    __tablename__ = 'tFamily'
    familyID = Column('familyID', Integer, primary_key=True)
    Column('familyName', String(255))
    Column('headofHouseID', Integer, ForeignKey('tHeadofHouse.headofHouseID'))

class tHeadofHouse(Base):
    __tablename__ = 'tHeadofHouse'
    headofHouseID = Column('headofHouseID', Integer, primary_key=True)
    Column('userID', Integer, ForeignKey('tUser.userID'))
 
Base.metadata.create_all(engine)
 
# Create a session
Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()

''' Example queries 
# Add a user
jwk_user = tUser(firstName='jesper', lastName='Krogh', email='jkrogh@gmail.com', password='spoopy', image = '')
session.add(jwk_user)
session.commit()
 
# Query the user
our_user = session.query(tUser).filter_by(firstName='jesper').first()
print('\nOur User:')
print(our_user)
'''