"""Home - Controller
from flask import Blueprint, request, render_template, flash, g, session, redirect

"""

from flask import Blueprint, render_template, request, redirect, session

from app.models.user import User

auth = Blueprint('Auth', __name__, url_prefix='/auth')


@auth.route('')
def index():
    """
    Index of Auth

    """
    if not request.form:
        return render_template('auth/login.html')
    return str(session)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Verify credentials and build the user session.

    """
    user = User.query.filter(User.email == request.form['email']).one()
    user.check_password(request.form['password'])
    if not user.check_password(request.form['password']):
        redirect('login-fail')
    session['authenticated'] = True
    session['user_id'] = user.id
    session['user_level'] = 'admin'
    return redirect('/dashboard')


@auth.route('/logout')
def logout():
    """
    Destroy all the sessions and log the user out.

    """
    session.clear()
    return redirect('/')


@auth.route('/sign-up')
def signup():
    """
    Sign up page route

    """
    return render_template('auth/sign-up.html')


@auth.route('/sign-up-submit', methods=['GET', 'POST'])
def signup_submit():
    """
    Route for user sign-up forms to go to.

    """
    if request.form['password'] != request.form['password2']:
        return redirect('/auth/sign-up-fail')
    already_signed_up = User.query.filter(User.email == request.form['email']).all()
    if len(already_signed_up) != 0:
        redirect('/auth/sign-up-fail')
    user = User()
    user.email = request.form['email']
    user.set_password(request.form['password'])
    user.save()
    return redirect('/dashboard')


@auth.route('/error')
def error():
    """
    Generic 403 Forbidden Error

    """
    return render_template('errors/403.html'), 403


# End File: stocky/app/controllers/auth.py
