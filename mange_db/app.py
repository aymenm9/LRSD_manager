from flask import Flask, session, render_template, redirect, request
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from models import Admin, Teachers, Departments, Grade
from db import db
from werkzeug.security import check_password_hash, generate_password_hash

# App config
app = Flask(__name__)

# Session config
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "/path/to/session/files"  # Update this path
Session(app)

# DB config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:aymen@localhost/lrsd'
db.init_app(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/add_admin", methods=["GET", "POST"])
def add_admin():
    if request.method == "GET":
        return redirect("/")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        new_admin = Admin(username=username, email=email, password_hash=generate_password_hash(password))
        db.session.add(new_admin)
        db.session.commit()
        return redirect("/")

@app.route("/add_department", methods=["GET", "POST"])
def add_department():
    if request.method == "GET":
        return redirect("/")
    else:
        name = request.form.get("name")
        new_department = Departments(name = name)
        db.session.add(new_department)
        db.session.commit()
        return redirect("/")
    
@app.route("/add_grade", methods=["GET", "POST"])
def add_grade():
    if request.method == "GET":
        return redirect("/")
    else:
        grade_ = request.form.get("grade")
        grade = Grade(grade = grade_)
        db.session.add(grade)
        db.session.commit()
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
