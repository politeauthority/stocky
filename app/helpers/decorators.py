"""Decorators

"""

from functools import wraps

from flask import session, redirect


def requires_auth(f):
    """
    Makes a method require a user to be logged in to access a method. If a user's not logged in they get an
    authentication error page.

    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' in session and session['user_id'] and session.get('authenticated'):
            return f(*args, **kwargs)
        else:
            return redirect('/auth/error'), 403
    return decorated
