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

tag_associate = db.Table('tag_associate',
    db.Column('post_id', db.Integer, db.ForeignKey('forum.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    info={'bind_key': 'forum_db'}
)

class Forum(db.Model):
    __bind_key__ = 'forum_db'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    datetime_start = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    datetime_end = db.Column(db.DateTime, nullable=True)
    banner_url = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(1000), nullable=False)
    body = db.Column(db.String(10000), nullable=False)
    tag = db.relationship('Tags', secondary = tag_associate, backref=db.backref('posts', lazy='dynamic'))

class Tags(db.Model):
    __bind_key__ = 'forum_db'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(100))

@app.route("/", methods=["GET"])
def index():
    db.create_all(bind=["forum_db"])
    #test_tag = Tags(tag = "bruh")
    #db.session.add(test_tag)
    #test_post = Forum(type="post", longitude=1.1, latitude=2.1, banner_url = "testurl", title = "test", body = "test")
    #db.session.add(test_post)
    #db.session.commit()
    this_tag = Tags.query.order_by(Tags.id).all()[0]
    this_post = Forum.query.order_by(Forum.id).all()[0]
    #this_tag.posts.append(this_post)
    #db.session.commit()

    #Try it out
    for post in this_tag.posts:
        print(post.id)
    return "test"

if __name__ == "__main__":
    app.run(debug=True)