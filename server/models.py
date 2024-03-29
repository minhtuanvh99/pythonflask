from server import db, login
from datetime import datetime
# some of hash method
from werkzeug.security import generate_password_hash, check_password_hash
# model need to inherit UserMixin to use extension
from flask_login import UserMixin
# 
from hashlib import md5
#
from time import time
import jwt
from server import app

# this method use to load user to flask-login
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# follower table have foreign key ref to User
# User relationship: many-to-many to itself  
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # 
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    # 
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    #
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
 
    #
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
 
    # get number of follower
    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    # get number of followed post
    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())      

    # hash password to a secret token
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
 
    # match secret token with a password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # get avatar from gravatar
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&amp;s={}'.format(
            digest, size)

    # create a token to verify user
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
 
    # verify token
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # reference to User table (User:1-Post:N)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
 
    def __repr__(self):
        return '<Post {}>'.format(self.body)


