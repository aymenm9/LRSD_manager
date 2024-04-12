
from flask import redirect, render_template, session
from functools import wraps
from db import db
from models import Admin, Teachers
from exceptions import Password_or_username_none, Pass_user_incorrect
from werkzeug.security import check_password_hash, generate_password_hash
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

def login_u(user_class,username, password):
    """sumary_line
            login function 
        Keyword arguments: user class , username , password
        argument -- user : Admin or Teatchers
        Return: user or raise Password_or_username_none or Pass_user_incorrect
    """
    if not (username and password):
        raise Password_or_username_none()
    if not (user := user_class.query.filter_by(username = username).first()):
        raise Pass_user_incorrect({"username": True , "msg":"username is incorect!"})
    if not check_password_hash(user.password_hash, password):
        raise Pass_user_incorrect({"password": True , "msg":"password is incorect!"})
    return user

def admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_type") != "admin":
            return redirect("/")
        return f(*args, **kwargs)