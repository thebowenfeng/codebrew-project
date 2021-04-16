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
    attendees = db.relationship('Events', secondary=events_user, backref=db.backref('attendees', lazy='dynamic'))


class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    b_name = db.Column(db.String(1000), nullable=False)
    suburb = db.Column(db.String(1000), nullable=False)
    dt = db.Column(db.DateTime, nullable=False)


class Suburbs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


@app.route("/", methods=["GET"])
def index():
    return "test"

if __name__ == "__main__":
    app.run(debug=True)