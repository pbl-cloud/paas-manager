from flask import session
from .models import Users


def current_user():
    if 'user_id' in session:
        return Users.find(session['user_id'])
    return None


def user_signed_in():
    return current_user() is not None
