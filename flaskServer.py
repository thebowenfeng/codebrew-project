from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

database_uri = "sqlite:///users.db"
#We need multiple databases
binds = {
    'forum_db' : 'sqlite:///forum.db',
}

app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
app.config["SQLALCHEMY_BINDS"] = binds
db = SQLAlchemy(app)
app.secret_key = "bruh"
#app.permanent_session_lifetime = timedelta(minutes=100) Optional maximum log in time before auto logging out

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"ID: {self.id} username: {self.username} password: {self.password}"

class Forum(db.Model):
    __bind_key__ = 'forum_db'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    banner_url = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(1000), nullable=False)
    body = db.Column(db.String(10000), nullable=False)
    tag = db.Column(db.String(1000), nullable=False)

@app.route("/", methods=["GET"])
def index():
    #db.create_all(bind="forum_db") Used to create databases
    return "test"

if __name__ == "__main__":
    app.run(debug=True)