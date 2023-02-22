from flask import Blueprint, render_template, redirect, url_for, session
views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("main/home.html")