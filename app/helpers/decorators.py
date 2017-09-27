"""
"""

from functools import wraps

from flask import session, redirect


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' in session and session['user_id'] and session.get('authenticated'):
            return f(*args, **kwargs)
        else:
            return redirect('/auth/error'), 403
    return decorated
