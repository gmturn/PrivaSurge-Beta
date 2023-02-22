from flask import Blueprint, render_template, request, flash, redirect, url_for, session, make_response, current_app
import MySQLdb.cursors
import re
from flaskapp import mysql, COOKIE_TIME_OUT
from functionality.user_functions import User

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email_username = request.form.get('email_username')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        email = email_username + "@privasurge.net"
        
        query_email = f"'{email}'"
        cursor = mysql.connection.cursor()
        cursor.execute(f"SELECT * FROM web_data.users WHERE email = {query_email}")
        account = cursor.fetchone()
        cursor.close()
        if account:
            flash('Account already exists', category='error')
        elif  re.match(r'[^@]+@[^@]+\.[^@]+', email_username):
            flash("Please do not include '@' or domain name in username", category='error')
        elif len(email_username) < 4:
            flash('Not a valid email address', category='error') # displays data on form - category name is irrelevant - used later to display messaged in differnt color
        elif len(firstName) < 2:
            flash('Not a valid First Name', category='error')
        elif not email_username or not password1 or not firstName or not lastName:
            flash('Please fill out form before submission')    
        elif password1 != password2:
            flash('Password\'s don\'t match', category='error')
        elif len(password1) < 7:
            flash('Insecure Password', category='error')
        else:
            flash('Email and Account created Successfully', category='success')

            newUser = User(email_username, email, password1)
            newUser.createWebUser(mysql, firstName, lastName)
            cursor = mysql.connection.cursor()
            cursor.execute(f"SELECT user_id FROM web_data.users WHERE email = {query_email};")
            uid = cursor.fetchone()
            if uid:
                stored_uid = uid[0]
            cursor.close()
            newUser.createUser(mysql, stored_uid)

    return render_template('auth/signup.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form #contains all the data in the form attribute
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember_user = request.form.get('remember_user')
        print(remember_user)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE email = % s AND password = % s;", (email, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['user_id']
            session['username'] = account['email']
            session['first_name'] = account['first_name']
            if remember_user:
                resp = make_response(redirect('/'))
                resp.set_cookie('email', account['email'], max_age=COOKIE_TIME_OUT)
                resp.set_cookie('passwordStored', password, max_age=COOKIE_TIME_OUT)
                resp.set_cookie('rem', 'checked', max_age=COOKIE_TIME_OUT)
                return resp

                
            flash('Logged in Successfully', category='success')
            return redirect(url_for('account.account', firstName = session['first_name']))
        else: 
            flash('Incorrect Email / Password Combination', category='error')

       
        cursor.close()
    return render_template('auth/login.html')


@auth.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('views.home'))