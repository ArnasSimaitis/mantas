from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class Groupuser(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.Integer)
    group = db.Column(db.Integer)

class Approvals(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    group = db.Column(db.Integer)
    user = db.Column(db.Integer)
    user_name = db.Column(db.String(150))
    admin = db.Column(db.Integer)
    group_name = db.Column(db.String(150))

class Groups(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(150))
    creator = db.Column(db.Integer)
    users = db.Column(db.Integer)

class Group_Bills(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150))
    sum = db.Column(db.Float)
    group = db.Column(db.Integer)
    user = db.Column(db.Integer)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    groups = db.Column(db.String())