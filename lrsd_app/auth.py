
from flask import redirect, render_template, session
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def admin(f):
    """chech if youser is admin
    
    Keyword arguments:  *args, **kwargs
    argument -- description
    Return: f return_description the origin function
    Return: redirct return_description redirct to "/"
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_type") != "admin":
            return redirect("/")
        return f(*args, **kwargs)