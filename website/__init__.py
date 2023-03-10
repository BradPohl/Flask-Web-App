# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 11:15:13 2023

@author: bpohl
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

"""
- Configure database, this will be skipped if database already exists
- run views and authorization for login
- fill database and login
"""
def create_app():
    app = Flask(__name__)   #initialize flask
    app.config['SECRET_KEY'] = 'shh...its a secret'    #Secure cookies
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    
    from .views import views
    from .auth import auth
    
    #run the views and authorization files
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    with app.app_context():
        db.create_all()


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app
