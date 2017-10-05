"""Home - Controller
from flask import Blueprint, request, render_template, flash, g, session, redirect

"""

from flask import Blueprint, render_template
from app.helpers.decorators import requires_auth

user = Blueprint('User', __name__, url_prefix='/profile')


@user.route('/settings')
@requires_auth
def settings():
    """
    Settings page

    """
    return render_template('user/settings.html')

# End File: stocky/app/controllers/user.py
