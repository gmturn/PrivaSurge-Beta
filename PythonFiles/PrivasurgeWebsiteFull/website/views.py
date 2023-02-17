from flask import Blueprint, render_template, redirect, url_for, session
views = Blueprint('views', __name__)

@views.route('/') #this is the decorator that says whenever this route is reached on website run this function ie whenever slash meaning the homepage @then the name of the view
def home():
    return render_template("home.html")

