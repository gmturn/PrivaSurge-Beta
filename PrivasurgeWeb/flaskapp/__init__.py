import os
from flask import Flask
from datetime import timedelta
from flask_mysqldb import MySQL

mysql = MySQL()
global COOKIE_TIME_OUT
#COOKIE_TIME_OUT = 60*60*24*7 #7 days
COOKIE_TIME_OUT = 60*5 #5 minutes

def create_app(test_config=None):
    #creates a flask instance
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = "lazyboy" # this encrypts website data like history and cookies
    app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=10)

    # setting up MySQL connection within flask
    app.config['MYSQL_HOST'] = '45.79.53.24'
    app.config['MYSQL_USER'] = 'remote_test'
    app.config['MYSQL_PASSWORD'] = 'Nielsen7579'
    app.config['MYSQL_DB'] = 'web_data'

    mysql.init_app(app)

    from .views import views
    from .auth import auth
    from .account import accountPage

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(accountPage, url_prefix='/')

    return app