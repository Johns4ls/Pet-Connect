from flask import flash, render_template, redirect, session, request
from app import app
from Modules import Tlbx, Database
from flask_login import login_required, logout_user, current_user
from Modules.forms import CreateFamilyForm, CreateDogForm, UserInfoForm
#Create a new User
@app.route('/Create/User', methods=['GET', 'POST'])
def userInfo():
    UserInfoform = UserInfoForm()
    if UserInfoform.validate_on_submit():
        firstName = UserInfoform.firstName.data
        lastName = UserInfoform.lastName.data
        email = session.get('email')
        password =  Tlbx.hash_password(session.get('password', None))
        address = UserInfoform.address.data
        addresslist = address.split('')
        address = addresslist[0]
        city = addresslist[1]
        state = addresslist[2]

        image = request.files[UserInfoform.profileImage.name]
        image = Tlbx.imgToJPG("Profile", image)
        Tlbx.new_Account(firstName, lastName, email, password, address, city, state, image)
        Tlbx.loginUser(email)
        return render_template('/Family/FamilySplash.html')
    flash("Please input data in all fields")
    return render_template('Register/userInfo.html', UserInfoform = UserInfoform)

@app.route('/Create/Start/Family', methods=['GET','POST'])
@login_required
def CreateNewFamily():
    CreateFamilyform = CreateFamilyForm()
    return render_template('/Family/FamilyCreate.html', CreateFamilyform = CreateFamilyform )

@app.route('/Create/Finish/Family', methods=['GET','POST'])
@login_required
def familyCreation():
    sqlalch = Database.Session()
    HeadOfHouse = Database.tHeadofHouse(userID = current_user.id)
    sqlalch.add(HeadOfHouse)
    id = sqlalch.commit()
    CreateFamilyform = CreateFamilyForm()
    if CreateFamilyform.validate_on_submit():
        CreateDogform = CreateDogForm()
        familyName = CreateFamilyform.surName.data
        cur, db = Tlbx.dbConnectDict()
        cursor= Database.Session()
        query = ("INSERT INTO tFamily (familyName, headofHouseID) VALUES(%s, %s);")
        data = (familyName, id)
        cur.execute(query, data)
        session['familyID'] = db.insert_id()
        x = cursor.query(Database.tUser).get(current_user.id)
        x.familyID = db.insert_id()
        cursor.commit()
        return render_template('Dog/NewDog.html', CreateDogform = CreateDogform)
    flash("Please add a family name")
    return render_template('/Family/FamilyCreate.html', CreateFamilyform = CreateFamilyform )


@app.route('/Join/Family/Landing', methods=['GET','POST'])
@login_required
def JoinFamilyLanding():
    return render_template('/Family/JoinFamily.html')

@app.route('/Join/Family/Search', methods=['GET','POST'])
@login_required
def JoinFamilySearch():
    session = Database.Session()
    Name = request.form['Search']
    Users = session.query(Database.tUser, Database.tFamily.familyName).join(Database.tHeadofHouse, Database.tHeadofHouse.userID == Database.tUser.userID) \
    .join(Database.tFamily, Database.tFamily.familyID == Database.tUser.userID) \
    .filter(Database.tFamily.familyName.contains(Name) | (Database.tUser.email.contains(Name)) \
    | (Database.tUser.email.op('SOUNDS LIKE')(Name))) \
    .order_by(Database.tFamily.familyName.contains(Name).desc()).all()

    return render_template('/Family/JoinFamilySearch.html', Users = Users)

@app.route('/Join/Family/<int:userID>', methods=['GET','POST'])
@login_required
def JoinFamily(userID):
    session = Database.Session()
    familyID = session.query(Database.tUser.familyID).filter(Database.tUser.userID == userID)
    for family in familyID:
        familyID = family.familyID
    x = session.query(Database.tUser).get(current_user.id)
    x.familyID = familyID
    session.commit()
    dogIDs = session.query(Database.tDog.dogID).filter(Database.tDog.familyID == familyID)
    for dogID in dogIDs:
        dog = Database.tFollowers(dogID = dogID.dogID, userID = current_user.id)
        session.add(dog)
        session.commit()
    return redirect('/dashboard')
