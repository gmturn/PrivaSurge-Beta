from flask import Blueprint, render_template, redirect, url_for, session, request
from functionality.user_functions import User
from flaskapp import mysql

accountPage = Blueprint('account', __name__)

@accountPage.route('/account')
def account():
    if 'loggedin' in session:
        return render_template("account/account.html")
    return redirect(url_for('auth.login'))

@accountPage.route('/accounts_email', methods=['GET', 'POST'])
def email_management():
    if 'loggedin' in session:
        aliasEmail = False
        if request.method == 'POST':
            form = request.form
            print(session['username'])
            print(session['id'])
            #userSession = User()
            #aliasEmail = userSession.generateTempEmail('Nielsen7579', 'Nielsen7579', 'jnielsen1919@gmail.com', 1)
            print(aliasEmail)
        return render_template('account/accounts_email.html')
    return redirect(url_for('auth.login'))