
from flask import redirect, render_template, session
from functools import wraps
from db import db
from models import Admin, Teachers
from exceptions import Password_or_username_none, Pass_user_incorrect
from werkzeug.security import check_password_hash
from apology import apology
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
def login_admin(f):
    """
    Decorate routes to require admin login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None or session.get("user_type") != "admin ":
            return apology("you are not alloed to be hier")
        return f(*args, **kwargs)

    return decorated_function

