from flask import Blueprint, render_template, redirect, url_for, session, request
from website.Functionality.userRegistration import User

accountPage = Blueprint('account', __name__)

@accountPage.route('/account')
def account():
    if 'loggedin' in session:
        return render_template("account.html")
    return redirect(url_for('auth.login'))


@accountPage.route('/accounts_email', methods=['GET', 'POST'])
def email_management():
    if 'loggedin' in session:
        aliasEmail = False
        if request.method == 'POST':
            form = request.form
            userSession = User()
            aliasEmail = userSession.createTempEmail('Nielsen7579', 'Nielsen7579', 'jnielsen1919@gmail.com', 1)
            print(aliasEmail)
        return render_template('accounts_email.html')
    return redirect(url_for('auth.login'))

