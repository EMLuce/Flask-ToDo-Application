'''Utilized to manipulate the back-end of all authentication views.'''
from flask_login import UserMixin
from app import db
from . import *

app = create_app

class User(db.Model, UserMixin):
    """This class is the user model that will hold all user data moving 
    forward."""
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    username = db.Column(db.String(150))
    password = db.Column(db.String(150))
    notes = db.relationship('Note')

class Note(db.Model):
    """This class is utilized to store all user To-Dos. A foreign
    key is utilized to form a relationship between To-dos and the User
    model."""
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.String(150))
    due_date = db.Column(db.String(150))
    note = db.Column(db.String(1000))
    completed = db.Column(db.Boolean, default=False, server_default="false")
    completed_date = db.Column(db.String(150), default='')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class FailedAttempts(db.Model):
    """This class is utilized to store security data. The intent is to
    have a log of every failed login attempt to prevent bruteforce attacks
    and limit vulnerabilities."""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150))
    ip = db.Column(db.Integer)
    date = db.Column(db.Integer)
    location = db.Column(db.String(300))