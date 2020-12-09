from server import db, login
from datetime import datetime
# some of hash method
from werkzeug.security import generate_password_hash, check_password_hash
# model need to inherit UserMixin to use extension
from flask_login import UserMixin


# this method use to load user to flask-login
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # 
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # hash password to a secret token
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
 
    # match secret token with a password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # reference to User table (User:1-Post:N)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
 
    def __repr__(self):
        return '<Post {}>'.format(self.body)


