from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

database_uri = "sqlite:///database.db"

app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
db = SQLAlchemy(app)
app.secret_key = "bruh"
#app.permanent_session_lifetime = timedelta(minutes=100) Optional maximum log in time before auto logging out

events_user = db.Table('events_user',
    db.Column('event_id', db.Integer, db.ForeignKey('events.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)


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


# not sure if done correctly. For now it checks with database and then adds user data to session for front end
@app.route("/user_login", methods=["POST"])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()  # might have issues with username that doesnt exist
        if user.password == password:
            session['user_data'] = user
        else:
            return 'Username or Password did not match'


if __name__ == "__main__":
    app.run(debug=True)