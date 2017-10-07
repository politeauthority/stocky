"""User - CONTROLLER

"""

from flask import Blueprint, render_template, request, redirect, session

from app.models.user import User
from app.helpers.decorators import requires_auth


user = Blueprint('User', __name__, url_prefix='/profile')


@user.route('/settings')
@requires_auth
def settings():
    """
    Settings page

    """
    d = {
        'user': User.query.filter(User.id == session['user_id']).one()
    }
    return render_template('user/settings.html', **d)


@user.route('/change-email')
@requires_auth
def change_email():
    return redirect('profile')


@user.route('/change-password', methods=['POST'])
@requires_auth
def change_password():
    """
    Change the user's password.
    @todo: Make sure that new_password and new_password_2 validate through frontend js.

    """
    if request.form['new_password'] != request.form['new_password_2']:
        # @todo: Notify user their new password wasnt validated.
        redirect('/profile/settings')

    # Check the user's current password matches.
    user = User.query.filter(User.id == session['user_id']).one()
    user.check_password(request.form['password'])
    if not user.check_password(request.form['password']):
        # @todo: Notify user the current password is wrong.
        redirect('/profile/settings')

    user.set_password(request.form['new_password'])
    user.save()

    # @todo: notify user password changed succesfully
    return redirect('profile')

# End File: stocky/app/controllers/user.py
