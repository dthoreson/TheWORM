from flask import render_template, request, redirect, session, flash

from flask_app import app

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask_app.models.user import User

#REDIRECT TO HOME PAGE---------
@app.route('/')
def index():
    return redirect('/main')


#HOME PAGE---------------
@app.route('/main')
def main():
    return render_template("index.html")


#PROCESS THAT RUNS WHEN YOU HIT REGISTER BUTTON----------
@app.route('/process/register', methods =['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    id = User.save_user(request.form)
    session['uid'] = id
    return redirect('/dashboard')


#PROCESS THAT RUNS WHEN YOU HIT LOGIN BUTTON-----------
@app.route('/process/login', methods =['POST'])
def login():
    logged_in_user = User.validate_login(request.form)
#THIS RUNS THE GET_BY_EMAIL CLS METHOD AND THE VALIDATE_LOGIN METHODS
    if not logged_in_user:
        return redirect('/')
#UID IS SHORT HAND FOR USER ID. THIS WILL KEEP TRACK OF USER LOGGED IN WITH SESSION.
    session['uid'] = logged_in_user.id
#SMALL CHECK TO ENSURE DATA IS BEING TRACKED PROPERLY
    print(logged_in_user.first_name)
    print(logged_in_user.id)
    return redirect('/dashboard')


#THIS IS WHAT DIRECTS US TO DASHBOARD AFTER THE PROCESSING OF REGISTER/LOGIN--------
@app.route('/dashboard')
def dashboard():
#THIS IS FOR DETECTING IF SOMEONE IS IN SESSION IN ORDER TO VIEW DASHBOARD PAGE.
    if not 'uid' in session:
        flash("Access Denied, please Login!")
        return redirect('/')
    data = {
        'id': session['uid']
    }
    return render_template("dashboard.html", logged_in_user=User.get_by_id(data)) #THIS JUST RENDERS THE DASHBOARD.HTML ONCE LOGGED IN


#THIS IS THE APP ROUTE FOR LOGOUT AND CLEARING SESSION.
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')