# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 11:17:09 2023

@author: bpohl
"""

#from website import database
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

"""
- Create a class that stores note's data
- Takes database
"""
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now()) #get current date and time
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #1 to many relationship, must be valid id

"""
- Create a class that stores the user's data
- Takes database and flask_login info
"""
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    
