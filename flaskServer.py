from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

database_uri = "sqlite:///database.db"

app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
db = SQLAlchemy(app)
app.secret_key = "bruh"
#app.permanent_session_lifetime = timedelta(minutes=100) Optional maximum log in time before auto logging out

suburbs_user = db.Table('suburbs_user',
    db.Column('suburb_id', db.Integer, db.ForeignKey('suburbs.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

events_user = db.Table('events_user',
    db.Column('event_id', db.Integer, db.ForeignKey('events.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

suburbs_org = db.Table('suburbs_org',
    db.Column('suburb_id', db.Integer, db.ForeignKey('suburbs.id')),
    db.Column('org_id', db.Integer, db.ForeignKey('organisation.id')),
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
    suburb = db.relationship('Suburbs', secondary=suburbs_user, backref=db.backref('users', lazy='dynamic'))
    attended = db.relationship('Events', secondary=events_user, backref=db.backref('attendees', lazy='dynamic'))


class Organisation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    suburb = db.relationship('Suburbs', secondary=suburbs_org, backref=db.backref('organisations', lazy='dynamic'))
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


@app.route("/", methods=["GET"])
def index():
    return "test"

if __name__ == "__main__":
    app.run(debug=True)