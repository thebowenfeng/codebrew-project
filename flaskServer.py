from flask import Flask, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest
import random
import os

#request = OrdersCreateRequest()

app = Flask(__name__)
database_uri = "sqlite:///database.db"
session = []
usrname = ""

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
scopes = ['https://www.googleapis.com/auth/calendar']

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    hs = db.Column(db.String(100), nullable=True)
    yr_lvl = db.Column(db.Integer, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    addr = db.Column(db.String(100), nullable=True)
    dt_start = db.Column(db.DateTime, nullable=True)
    dt_end = db.Column(db.DateTime, nullable=True)
    suburb_id = db.Column(db.Integer, db.ForeignKey("suburbs.id"))
    user_range = db.Column(db.Integer, nullable=False)
    attended = db.relationship('Events', secondary=events_user, backref=db.backref('attendees', lazy='dynamic'))


class Organisation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    suburb_id = db.Column(db.Integer, db.ForeignKey("suburbs.id"))
    events = db.relationship('Events', backref='organisation')
    isEvent = db.Column(db.Boolean, nullable=False)  # says if organisation is making the next week event


class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(db.Integer, db.ForeignKey('organisation.id'))  # suburb info can be obtained from organisation
    event_name = db.Column(db.String(1000), nullable=False)
    dt_begin = db.Column(db.DateTime, nullable=False)
    dt_end = db.Column(db.DateTime, nullable=True)
    addr = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(10000), nullable=False)
    vol_num = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, nullable=False)


class Suburbs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    postcode = db.Column(db.Integer, nullable=False)
    users = db.relationship("Users", backref="suburb")
    orgs = db.relationship("Organisation", backref="suburb")


# Gets range in km between 2 suburbs
def georange(Suburb1, Postcode1, Suburb2, Postcode2):
    location1 = geolocator.geocode(f'{Suburb1} {Postcode1}')
    location2 = geolocator.geocode(f'{Suburb2} {Postcode2}')
    return geodesic(location1, location2)


def search_georange(location1, Suburb2, Postcode2):
    location2 = geolocator.geocode(f'{Suburb2} {Postcode2}')
    return geodesic(location1, location2).km


@app.route("/", methods=["GET"])
def index():
    return """<!DOCTYPE html>

<head>
  <meta name="viewport" content="width=device-width, initial-scale=1"> <!-- Ensures optimal rendering on mobile devices. -->
  <meta http-equiv="X-UA-Compatible" content="IE=edge" /> <!-- Optimal Internet Explorer compatibility -->
</head>

<body>
  <script
    src="https://www.paypal.com/sdk/js?client-id=Ab-TmVOOF38HXqyvqZN8T5pvj_mgN5WYSW2RE7kbwLoFFYqVB18CF7bMrWtZAjp-8IzZnYUsx2VELDBf"> // Required. Replace YOUR_CLIENT_ID with your sandbox client ID.
  </script>
  <script>
    paypal.Buttons({
    createOrder: function(data, actions) {
      // This function sets up the details of the transaction, including the amount and line item details.
      return actions.order.create({
        purchase_units: [{
          amount: {
            value: '100'
          }
        }]
      });
    },
    onApprove: function(data, actions) {
      // This function captures the funds from the transaction.
      return actions.order.capture().then(function(details) {
        // This function shows a transaction success message to your buyer.
        alert('Transaction completed by ' + details.payer.name.given_name);
      });
    }
  }).render('body');
  </script>
</body>"""


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
                response["password"] = user.password
                response["type"] = user.type
                response["suburb"] = (Suburbs.query.get(user.suburb_id)).name
                response["postcode"] = (Suburbs.query.get(user.suburb_id)).postcode
                response["range"] = user.user_range
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
                response["username"] = user.username
                response["password"] = user.password
                response["name"] = user.name
                #response["events"] = user.events  # might not work if there is none
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
        firstname = request.form["firstname"]
        surname = request.form["surname"]
        hs = request.form["highschool"]
        yrlvl = int(request.form["yearlevel"])
        longtitude = request.form["long"]
        latitude = request.form["lat"]
        user_range = request.form["range"]

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

        this_user = Users(type = "student", username=username, password=password, firstname=firstname, surname=surname, hs=hs, yr_lvl=yrlvl, suburb=this_suburb, user_range=user_range)
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
        firstname = request.form["firstname"]
        surname = request.form["surname"]
        age = int(request.form["age"])
        addr = request.form["address"]
        longtitude = request.form["long"]
        latitude = request.form["lat"]
        user_range = request.form["range"]

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

        this_user = Users(type = "mentor", username=username, password=password,firtname=firstname, surname=surname, age=age, addr=addr, suburb=this_suburb, user_range=user_range)
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

        this_org = Organisation(name = name, username=username, password=password, suburb=this_suburb, isEvent=False)
        db.session.add(this_org)
        db.session.commit()

        response["status"] = "success"
        return jsonify(response)

    else:
        return "Error: Unsupported request method"


@app.route("/create_event", methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        response = {}
        username = request.form['username']
        password = request.form['password']
        for user in Organisation.query.all():
            if user.username == username and user.password == password:
                if user.isEvent:
                    name = request.form['event_name']
                    begin = datetime.strptime(request.form["event_begin"], '%d/%m/%y %H:%M:%S')

                    if 'event_end' in request.form:
                        end = datetime.strptime(request.form["event_end"], '%d/%m/%y %H:%M:%S')
                    else:
                        end = None

                    addr = request.form['address']
                    desc = request.form['description']
                    vol_num = request.form['volunteer_num']

                    new_event = Events(organisation=user, event_name=name, dt_begin=begin, dt_end=end, addr=addr, desc=desc, vol_num=vol_num, completed=False)
                    user.isEvent = False
                    db.session.add(new_event)
                    db.session.commit()

                    # ----------------- ADDING USERS TO EVENT ------------------ #
                    volunteers = []

                    for volunteer in Users.query.all():
                        loc_range = georange(volunteer.suburb.name, volunteer.suburb.postcode, user.suburb.name, user.suburb.postcode)  # gets distance between user and event
                        if volunteer.range <= loc_range:  # checks if within range
                            volunteers.append(volunteer)

                    if len(volunteers) > vol_num:
                        num1 = vol_num
                    else:
                        num1 = len(volunteers)

                    while num1 > 0:
                        volunteer = random.choice(volunteers)
                        volunteer. attended.append(new_event)
                        volunteers.remove(volunteer)
                        num1 -= 1
                    db.session.commit()
                    # ----------------- ADDING USERS TO EVENT ------------------ #

                    response['status'] = 'success'
                    return jsonify(response)
                else:
                    response['status'] = 'failure'
                    response['error'] = 'Organisation is not eligible to create a new event this week'
                    return jsonify(response)
            else:
                response['status'] = 'failure'
                response['error'] = 'Issue with user information'
                return jsonify(response)
    else:
        return "Error: unsupported request method"


@app.route("/update_user", methods=["GET", "POST"])
def update_user():
    if request.method == "POST":
        response = {}

        username = request.form["username"]
        password = request.form["password"]

        if username == "" or password == "":
            response["status"] = "failure"
            response["error"] = "Empty fields"

        addr = request.form["address"]
        hs = request.form["highschool"]
        yrlvl = request.form["yearlevel"]

        dt_start = datetime.strptime(request.form["startdate"], '%d/%m/%y %H:%M:%S')
        dt_end = datetime.strptime(request.form["enddate"], '%d/%m/%y %H:%M:%S')

        if request.form["startdate"] == "":
            dt_start = None
        if request.form["enddate"] == "":
            dt_end = None

        suburb = request.form["suburb"] # CHECK IF A SUBURB EXISTS USING BOTH SUBURB AND POSTCODE
        postcode = int(request.form["postcode"])

        this_user = Users.query.filter_by(username=username).first()
        this_user.username = username
        this_user.password = password
        this_user.addr = addr
        this_user.hs = hs
        this_user.yr_lvl = int(yrlvl)
        this_user.dt_start = dt_start
        this_user.dt_end = dt_end

        for i in Suburbs.query.all():
            if i.name == suburb and i.postcode == postcode:
                this_user.suburb = i
                break

        db.session.commit()
        response["status"] = "success"
        return jsonify(response)
    else:
        return "Error: Unsupported request method"

@app.route('/search', methods=['GET', 'POST'])  # NEEDS TESTING
def search():
    if request.method == 'POST':
        response = {}

        addr = request.form["address"]
        search_range = request.form["range"]

        try:
            location = geolocator.geocode(addr)
        except:
            response['status'] = 'failure'
            response['error'] = 'Not a valid location'
            return jsonify(response)

        events = []
        suburbs = []

        for suburb in Suburbs.query.all():
            distance = search_georange(location, suburb.name, suburb.postcode)
            if distance <= search_range:
                suburbs.append(suburb)

        for event in Events.query.filter_by(completed=False).all():
            if Suburbs.query.get(event.organisation.suburb_id) in suburbs:
                event_dict = {}
                event_dict['event_id'] = event.id
                event_dict['org_id'] = event.org_id
                event_dict['event_name'] = event.event_name
                event_dict['begin'] = event.dt_begin
                event_dict['end'] = event.dt_end
                event_dict['address'] = event.addr
                events.append(jsonify(event_dict))

        response['status'] = 'success'
        response["events"] = events
        return jsonify(response)
    else:
        return "Error: Unsupported request method"

@app.route('/set_events', methods=['GET', 'POST']) # NEEDS TESTING
def set_events():
    if request.method == 'POST':
        response = {}
        if request['token'] == 'bruh':  # potentially could make this a secret variable (if we want)
            for user in Organisation.query.all():
                user.isEvent = False

            for suburb in Suburbs.query.all():
                org_list = suburb.orgs
                chosen_org = random.choice(org_list)
                chosen_org.isEvent = True

            response['status'] = 'success'
            return jsonify(response)
        else:
            response['status'] = 'failure'
            response['error'] = 'Not valid token'
            return jsonify(response)
    else:
        return "Error: Unsupported request method"

@app.route('/calendar', methods=["GET", "POST"])
def calendar():
    global session
    global usrname
    if request.method == "POST":
        usrname = request.form["username"]

        flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)
        flow.redirect_uri = url_for('calendar_callback', _external=True)
        authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
        session.append(state)
        return jsonify({"url" : authorization_url})
    else:
        return "Error: Unsupported request method"

@app.route("/calendar_callback", methods=['GET', 'POST'])
def calendar_callback():
    global session
    global usrname
    if request.method == "GET":
        state = session[0]
        session = []
        username = usrname

        flow = Flow.from_client_secrets_file('client_secret.json', scopes=scopes, state=state)
        flow.redirect_uri = url_for('calendar_callback', _external=True)
        auth_response = request.url
        flow.fetch_token(authorization_response=auth_response)

        cred = flow.credentials

        service = build("calendar", "v3", credentials=cred)

        user = Users.query.filter_by(username=username).first()
        event_obj = list(user.attended)[-1]

        cal_event = {
            'summary': event_obj.event_name,
            'location': event_obj.addr,
            'description': 'A chance to hear more about Google\'s developer products.',
            'start': {
                'dateTime': event_obj.dt_begin.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': 'Australia/Melbourne',
            },
            'end': {
                'dateTime': event_obj.dt_end.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': 'Australia/Melbourne',
            },
            'reminders': {
                'useDefault': True
            },
        }

        event = service.events().insert(calendarId='primary', body=cal_event).execute()
        print("Event created")

        return "Success"
    else:
        return "Error: Unsupported request method"

@app.route('/get_event', methods=['GET', 'POST'])
def get_event():
    if request.method == 'POST':
        response = {}
        event_id = request.form['event_id']
        event = Events.query.get(event_id)
        try:
            response['event_id'] = event.id
            response['org_id'] = event.org_id
            response['event_name'] = event.event_name
            response['begin'] = event.dt_begin
            response['end'] = event.dt_end
            response['address'] = event.addr
            response['description'] = event.desc
            response['completed'] = event.completed
            return(jsonify(response))
        except:
            response['status'] = 'failure'
            response['error'] = 'invalid event ID'
            return jsonify(response)
    else:
        return "Error: Unsupported request method"

if __name__ == "__main__":
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    app.run(debug=True)