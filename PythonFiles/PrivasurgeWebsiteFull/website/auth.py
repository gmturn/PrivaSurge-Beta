from flask import Blueprint, render_template, request, flash, redirect, url_for, session, make_response
from website import COOKIE_TIME_OUT
from website.database import mysql
import MySQLdb.cursors
import re

auth = Blueprint('auth', __name__)

#whenever you render html in flask it is called a template and it is a special language called jinga - templates folder

@auth.route('/login', methods=['GET', 'POST']) #this is how you create different pages - telling flask what kind of http requests we can handle on these pages - note same on sign up page
def login(): #best practice to name the function after the route
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
    return render_template('login.html')


@auth.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return render_template('home.html')


@auth.route('/signup', methods=['GET', 'POST']) 
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = % s;", (email, ))
        account = cursor.fetchone()
        cursor.close()
        if account:
            flash('Account already exists', category='error')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Please enter a valid email address', category='error')
        elif len(email) < 4:
            flash('Not a valid email address', category='error') # displays data on form - category name is irrelevant - used later to display messaged in differnt color

        elif len(firstName) < 2:
            flash('Not a valid First Name', category='error')
        elif not email or not password1 or not firstName or not lastName:
            flash('Please fill out form before submission')    
        elif password1 != password2:
            flash('Password\'s don\'t match', category='error')
            
        elif len(password1) < 7:
            flash('Insecure Password', category='error')
            
        else:
            #if doesnt exists already -> create new account
            flash('Account created successfully', category='success')
            #add user to database

            cursor = mysql.connection.cursor()
            sql = f"""
                INSERT INTO users (email, password, first_name, last_name)
                    VALUES ("{email}", "{password1}", "{firstName}", "{lastName}")
            """
            cursor.execute(sql)
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('auth.login'))

    return render_template('sign-up.html')


