from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    """
    Flask-login uses this callback function to retrieve a user when a unique identifier is passed.

    :param user_id: user id
    :return:
    """
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    def __init__(self, email, username, password):
        self.password = password
        self.email = email
        self.username = username

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    username = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    firstname = db.Column(db.String(255))
    pitches = db.relationship('Pitch', backref='owner', lazy="dynamic")
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    reviews = db.relationship('Review', backref='user', lazy="dynamic")
    votes = db.relationship('Vote', backref='user_vote', lazy="dynamic")

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    def __repr__(self):
        return f'User {self.username}'


class Pitch(db.Model):
    """
    Pitch model
    """
    __tablename__ = 'pitch'

    id = db.Column(db.Integer, primary_key=True)
    audio_url = db.Column(db.String)
    name = db.Column(db.String(50))
    description = db.Column(db.Text())
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    votes = db.relationship('Vote', backref='pitch_vote', lazy="dynamic")

    # pitch = Pitch()
    # you have access to pitch.owner
    def __init__(self, name, description, owner_id):
        self.name = name
        self.description = description
        self.owner_id = owner_id

    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'Pitch {self.name}'


class Role(db.Model):
    """
    Roles
    """
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    users = db.relationship('User', backref='role', lazy="dynamic")

    def __repr__(self):
        return f'Role {self.name}'


class Review(db.Model):
    """
    Review model
    """
    __tablename__ = 'review'
    all_reviews = []

    def __init__(self, pitch_id, pitch_review, user_id):
        self.pitch_review = pitch_review
        self.pitch_id = pitch_id
        self.user_id = user_id

    id = db.Column(db.Integer, primary_key=True)
    pitch_id = db.Column(db.Integer, db.ForeignKey("pitch.id"))
    pitch_review = db.Column(db.String)
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    @classmethod
    def clear_reviews(cls):
        Review.all_reviews.clear()

    def save_review(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_reviews(cls, id):
        reviews = Review.query.filter_by(pitch_id=id).all()
        return reviews


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pitch_id = db.Column(db.Integer, db.ForeignKey("pitch.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    type = db.Column(db.String)

    def save_vote(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_vote_count(cls, id):
        return db.session.query(
            Vote.type,
            func.count(Vote.type)
        ).filter_by(pitch_id=id).group_by(Vote.type).all()

    def __repr__(self):
        return f'Vote {self.type}'
