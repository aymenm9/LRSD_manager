from flask import Flask , session, render_template, redirect , request, jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from models import Admin, Teachers, Departments
from db import db
from auth import login_required,admin, login_u
from apology import apology
from werkzeug.security import check_password_hash, generate_password_hash
from exceptions import Password_or_username_none, Pass_user_incorrect
# app config
app = Flask(__name__)

# session config 
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# DB config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:aymen@localhost/lrsd'
db.init_app(app)

@app.route('/')
@login_required
def index():
    if session["user_type"] == "admin": 
        return redirect("/admin_dashboard")
    else:
        return apology("not created yet")
         
@app.route("/admin_dashboard")
@login_required
def admin_dashboard():
    teachers = teachers = Teachers.query.with_entities(Teachers.first_name,Teachers.last_name,Teachers.username ,Teachers.id).all()
    return render_template("admin_dashboard.html",departments = Departments.query.all(), teachers = teachers)

@app.route("/add_teacher", methods=["GET","POST"])
@login_required
def add_teacher():
    if request.method == "GET":
        redirect("/")
    else:
        if not((username := request.form.get("username")) and (password := request.form.get("password")) and (department := request.form.get("department"))):
            return apology("one is blank")
        
        if email := request.form.get("email") : 
            teacher = Teachers(username = username , email = email , password_hash = generate_password_hash(password), department_id = department)
        db.session.add(teacher)
        db.session.commit()
        return redirect("/")

"""@app.route("/teachers_list")
def teachers_list():
    return render_template("teachers_list.html")"""

@app.route("/teachers_list")
@login_required
def teachers_list():
    teachers = Teachers.query.with_entities(Teachers.first_name,Teachers.last_name,Teachers.username).all()
    return render_template("teachers_list.html", teachers= teachers)
    


@app.route("/login")
def login():
    session.clear()
    return render_template("login.html")

@app.route("/login_admin", methods=["GET","POST"])
def login_admin():
    session.clear()
    if request.method == "GET":
        redirect("/") 
    else:
        try:
            user = login_u(Admin, request.form.get("username"), request.form.get("password"))
        except Password_or_username_none or Pass_user_incorrect as e:
            return apology(e.error["msg"])
        session["user_id"] = user.id
        session["user_type"] = "admin"
        return redirect('/')

@app.route("/login_teacher", methods=["GET","POST"])
def login_teacher():
    session.clear()
    if request.method == "GET":
        return redirect("/") 
    else:
        try:
            user = login_u(Teachers, request.form.get("username"), request.form.get("password"))
        except Password_or_username_none or Pass_user_incorrect as e:
            return apology(e.error["msg"])
        session["user_id"] = user.id
        session["user_type"] = "teachers"
        return redirect('/')


@app.route("/logout", methods=["GET","POST"])
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
