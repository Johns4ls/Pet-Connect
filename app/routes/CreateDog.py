from Modules import Database, Tlbx
from flask_login import login_required, current_user
from flask import redirect, request, render_template, flash, session
from app import app
from Modules.forms import CreateDogForm, FavoriteParkForm
from Follow import FollowDogs
@app.route('/Create/New/Dog', methods=['GET','POST'])
@login_required
def CreateNewDog():
    session = Database.Session()
    headOfHouse = session.query(Database.tHeadofHouse).filter(Database.tHeadofHouse.userID == current_user.id).all()
    if headOfHouse == []:
        flash("You must be the head of household to create a new dog")
        return redirect('/dashboard')
    followed = session.query(Database.tDog.dogID).join(Database.tUser, Database.tDog.familyID == Database.tUser.familyID) \
    .filter(Database.tUser.userID == current_user.id)
    CreateDogform = CreateDogForm()
    if followed is not None:
        return render_template('Dog/NewDog.html', CreateDogform = CreateDogform)
    else:
        return render_template('Dog/Initial_NewDog.html', CreateDogForm = CreateDogform)

@app.route('/Create/Start/Park', methods=['GET','POST'])
@login_required
def StartPark():
    CreateDogform = CreateDogForm()
    dbsession = Database.Session()
    if CreateDogform.validate_on_submit():
        session['dogName'] = CreateDogform.dogName.data
        session['gender'] = CreateDogform.gender.data
        session['breed'] = CreateDogform.breed.data
        session['fixed'] = CreateDogform.fixed.data
        session['age'] = CreateDogform.age.data
        session['favToy'] = CreateDogform.favToy.data
        session['size'] = CreateDogform.size.data
        session['weight'] = CreateDogform.weight.data
        session['bio'] = CreateDogform.bio.data
        image = request.files[CreateDogform.profileImage.name]
        session['image'] = Tlbx.imgToJPG("Profile", image)
        FavoriteParkform = FavoriteParkForm()
        followed = dbsession.query(Database.tDog.dogID).join(Database.tUser, Database.tDog.familyID == Database.tUser.familyID) \
        .filter(Database.tUser.userID == current_user.id)
        if followed is not None:
            return render_template('/Dog/NewPark.html', FavoriteParkform = FavoriteParkform)
        else:
            return render_template('Dog/Initial_NewPark.html', FavoriteParkform = FavoriteParkform)
        return render_template('/Dog/NewPark.html', FavoriteParkform = FavoriteParkform)
    flash("Please fill out all fields")
    if followed is not None:
        return render_template('Dog/NewDog.html', CreateDogform = CreateDogform)
    else: 
        return render_template('/Dog/Initial_NewDog.html', CreateDogForm = CreateDogForm)


@app.route('/Create/Finish/Dog', methods=['GET','POST'])
@login_required
def DogCreation():
    FavoriteParkform = FavoriteParkForm()
    if FavoriteParkform.validate_on_submit():
        #insert Breed
        cur, db = Tlbx.dbConnectDict()
        breedQuery = "INSERT INTO tBreed (breed) VALUES (%s);"
        data = (session.get('breed'))
        cur.execute(breedQuery, data)
        db.commit()
        breedID = cur.lastrowid

        #Insert Address then insert Favorite Park
        image = None
        addressQuery = "INSERT INTO tAddress (address, city, state) VALUES (%s, %s, %s);"

        addresslist = (FavoriteParkform.address.data).split(',')
        address = addresslist[0]
        city = addresslist[1]
        state = addresslist[2]
        data = (address, city, state)
        cur.execute(addressQuery, data)
        favParkQuery = "INSERT INTO tFavoritePark (parkName, AddressID, image) VALUES (%s, LAST_INSERT_ID(), %s);"
        data = (FavoriteParkform.parkName.data, image)
        cur.execute(favParkQuery, data)
        db.commit()
        favParkID = cur.lastrowid

        #Insert favorite toy.
        image = None
        favToyQuery = "INSERT INTO tFavoriteToy (ToyName, image) VALUES (%s, %s);"
        data = (session['favToy'], image)
        cur.execute(favToyQuery, data)
        db.commit()
        favToyID = cur.lastrowid
        cursor = Database.Session()
        familyID = session.get('familyID')
        if familyID is None:
            familyID = cursor.query(Database.tUser.familyID).filter(Database.tUser.userID == current_user.id)
            for familyID in familyID:
                familyID = familyID.familyID

        # commit all the dog data into the database.
        dogQuery = "Insert into tDog (name, gender, breedID, fixed, age, Size, Weight, bio, image, favToyID, favParkID, familyID) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s)"
        data = (session.get('dogName'), session.get('gender'), breedID, session.get('fixed'), session.get('age'), session.get('size'), session.get('weight'), session.get('bio'), session.get('image'), favToyID, favParkID, familyID )
        cur.execute(dogQuery, data)
        db.commit()

        #Follow the dog
        sqlalch = Database.Session()
        Query = Database.tFollowers(dogID=cur.lastrowid, userID=current_user.id)
        sqlalch.add(Query)
        sqlalch.commit()
        return redirect('/dashboard')
    flash("please input your dogs favorite park")
    return render_template('/Dog/NewPark.html', FavoriteParkform = FavoriteParkform)

    #finally commit all the dog data into the database.
    dogQuery = "Insert into tDog (name, gender, breedID, fixed, age, Size, Weight, bio, image, favToyID, favParkID, familyID) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s)"
    data = (session.get('dogName'), session.get('gender'), breedID, session.get('fixed'), session.get('age'), session.get('size'), session.get('weight'), session.get('bio'), image, favToyID, favParkID, session.get('familyID') )
    cur.execute(dogQuery, data)
    db.commit()

    #Default to follow the dog
    dogID = cur.lastrowid
    FollowDogs(dogID)

    #Redirect to the dashboard
    return redirect('/dashboard')

    