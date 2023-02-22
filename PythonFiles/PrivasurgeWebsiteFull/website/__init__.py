#creates a python package out of website folder
from flask import Flask
from flask_mysqldb import MySQL
from flask_login import LoginManager
from datetime import timedelta



app = Flask(__name__) #how to initialize flask
app.config['SECRET_KEY'] = "lazyboy" # this encrypts website data like history and cookies
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=10)
app.config['MYSQL_HOST'] = '45.79.53.24'
app.config['MYSQL_USER'] = 'remote_test'
app.config['MYSQL_PASSWORD'] = 'Nielsen7579'
app.config['MYSQL_DB'] = 'web_data'
mysql = MySQL(app)

from views import views
from auth import auth
from account import accountPage

app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/') #prefix shows accesss to the views stored in the file - will be shown whenever the url is in the window
app.register_blueprint(accountPage, url_prefix='/')


