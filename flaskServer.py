from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from geopy.geocoders import Nominatim

app = Flask(__name__)

database_uri = "sqlite:///database.db"

app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
db = SQLAlchemy(app)
app.secret_key = "bruh"
#app.permanent_session_lifetime = timedelta(minutes=100) Optional maximum log in time before auto logging out
app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)

events_user = db.Table('events_user',
    db.Column('event_id', db.Integer, db.ForeignKey('events.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

geolocator = Nominatim(user_agent="codebrew_project")

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    hs = db.Column(db.String(100), nullable=True)
    yr_lvl = db.Column(db.Integer, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    addr = db.Column(db.String(100), nullable=True)
    suburb_id = db.Column(db.Integer, db.ForeignKey("suburbs.id"))
    attended = db.relationship('Events', secondary=events_user, backref=db.backref('attendees', lazy='dynamic'))


class Organisation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    suburb_id = db.Column(db.Integer, db.ForeignKey("suburbs.id"))
    events = db.relationship('Events', backref='organisation')


class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(db.Integer, db.ForeignKey('organisation.id'))
    event_name = db.Column(db.String(1000), nullable=False)
    suburb = db.Column(db.String(1000), nullable=False)
    dt_begin = db.Column(db.DateTime, nullable=False)
    dt_end = db.Column(db.DateTime, nullable=True)
    addr = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(10000), nullable=False)


class Suburbs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    postcode = db.Column(db.Integer, nullable=False)
    users = db.relationship("Users", backref="suburb")
    orgs = db.relationship("Organisation", backref="suburb")


@app.route("/", methods=["GET"])
def index():
    return "test"


@app.route("/user_login", methods=["GET", "POST"])
def user_login():
    if request.method == 'POST':
        response = {}
        username = request.form['username']
        password = request.form['password']
        for user in Users.query.all():
            if user.username == username and user.password == password:
                response["status"] = "success"
                response["username"] = user.username
                response["type"] = user.type
                response["suburb"] = (Suburbs.query.get(user.suburb_id)).name
                response["postcode"] = (Suburbs.query.get(user.suburb_id)).postcode
                if user.type == 'student':
                    response["high_school"] = user.hs
                    response["year_level"] = user.yr_lvl
                elif user.type == 'mentor':
                    response["address"] = user.addr
                    response["age"] = user.age
                return jsonify(response)

        response["status"] = "failure"
        return jsonify(response)
    else:
        return "Error: unsupported request method"


@app.route("/org_login", methods=["GET", "POST"])
def org_login():
    if request.method == 'POST':
        response = {}
        username = request.form['username']
        password = request.form['password']
        for user in Organisation.query.all():
            if user.username == username and user.password == password:
                response["status"] = "success"
                response["name"] = user.username
                response["events"] = user.events  # might not work if there is none
                response["suburb"] = (Suburbs.query.get(user.suburb_id)).name
                response["postcode"] = (Suburbs.query.get(user.suburb_id)).postcode
                return jsonify(response)

        response["status"] = "failure"
        return jsonify(response)
    else:
        return "Error: unsupported request method"


@app.route("/student_signup", methods=["GET", "POST"])
def student_signup():
    if request.method == "POST":
        response = {}
        username = request.form["username"]
        password = request.form["password"]
        hs = request.form["highschool"]
        yrlvl = int(request.form["yearlevel"])
        longtitude = request.form["long"]
        latitude = request.form["lat"]

        if username == "" or password == "":
            response["status"] = "failure"
            response["error"] = "Empty fields"
            return jsonify(response)

        if Users.query.filter_by(username=username).first() != None:
            response["status"] = "failure"
            response["error"] = "Duplicate username"
            return jsonify(response)


        long_lat = f"{latitude}, {longtitude}"
        try:
            location = geolocator.reverse(long_lat)
            suburb = location.raw["address"]["suburb"]
            postcode = int(location.raw["address"]["postcode"])
        except:
            response["status"] = "failure"
            response["error"] = "Invalid location"
            return jsonify(response)

        if Suburbs.query.filter_by(name=suburb).first() == None:
            this_suburb = Suburbs(name=suburb, postcode=postcode)
            db.session.add(this_suburb)
            db.session.commit()
        else:
            this_suburb = Suburbs.query.filter_by(name=suburb).first()

        this_user = Users(type = "student", username=username, password=password, hs=hs, yr_lvl=yrlvl, suburb=this_suburb)
        db.session.add(this_user)
        db.session.commit()

        response["status"] = "success"
        return jsonify(response)

    else:
        return "Error: Unsupported request method"


@app.route("/mentor_signup", methods=["GET", "POST"])
def mentor_signup():
    if request.method == "POST":
        response = {}
        username = request.form["username"]
        password = request.form["password"]
        age = int(request.form["age"])
        addr = request.form["address"]
        longtitude = request.form["long"]
        latitude = request.form["lat"]

        if username == "" or password == "":
            response["status"] = "failure"
            response["error"] = "Empty fields"
            return jsonify(response)

        if Users.query.filter_by(username=username).first() != None:
            response["status"] = "failure"
            response["error"] = "Duplicate username"
            return jsonify(response)

        long_lat = f"{latitude}, {longtitude}"
        try:
            location = geolocator.reverse(long_lat)
            suburb = location.raw["address"]["suburb"]
            postcode = int(location.raw["address"]["postcode"])
        except:
            response["status"] = "failure"
            response["error"] = "Invalid location"
            return jsonify(response)

        if Suburbs.query.filter_by(name=suburb).first() == None:
            this_suburb = Suburbs(name=suburb, postcode=postcode)
            db.session.add(this_suburb)
            db.session.commit()
        else:
            this_suburb = Suburbs.query.filter_by(name=suburb).first()

        this_user = Users(type = "mentor", username=username, password=password, age=age, addr=addr, suburb=this_suburb)
        db.session.add(this_user)
        db.session.commit()

        response["status"] = "success"
        return jsonify(response)

    else:
        return "Error: Unsupported request method"


@app.route("/org_signup", methods=["GET", "POST"])
def org_signup():
    if request.method == "POST":
        response = {}
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]
        longtitude = request.form["long"]
        latitude = request.form["lat"]

        if username == "" or password == "" or name == "":
            response["status"] = "failure"
            response["error"] = "Empty fields"
            return jsonify(response)

        if Organisation.query.filter_by(username=username).first() != None:
            response["status"] = "failure"
            response["error"] = "Duplicate username"
            return jsonify(response)

        long_lat = f"{latitude}, {longtitude}"
        try:
            location = geolocator.reverse(long_lat)
            suburb = location.raw["address"]["suburb"]
            postcode = int(location.raw["address"]["postcode"])
        except:
            response["status"] = "failure"
            response["error"] = "Invalid location"
            return jsonify(response)

        if Suburbs.query.filter_by(name=suburb).first() == None:
            this_suburb = Suburbs(name=suburb, postcode=postcode)
            db.session.add(this_suburb)
            db.session.commit()
        else:
            this_suburb = Suburbs.query.filter_by(name=suburb).first()

        this_org = Organisation(name = name, username=username, password=password, suburb=this_suburb)
        db.session.add(this_org)
        db.session.commit()

        response["status"] = "success"
        return jsonify(response)

    else:
        return "Error: Unsupported request method"


if __name__ == "__main__":
    app.run(debug=True)