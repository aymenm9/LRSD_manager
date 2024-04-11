from flask import Flask , session, render_template, redirect , request
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from models import Admin, Teachers, Departments
from db import db
from auth import login_required,admin
from apology import apology
from werkzeug.security import check_password_hash, generate_password_hash
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
    return render_template("admin_dashboard.html",departments = Departments.query.all())

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



@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login_admin", methods=["GET","POST"])
def login_admin():
    session.clear()
    if request.method == "GET":
        redirect("/") 
    else:
        #todo implement login
        if not ((username := request.form.get("username")) and (password := request.form.get("password"))):
            return apology("user or pass is blank!")
        if not (admin := Admin.query.filter_by(username = username).first()):
            return apology("user is incorect!")
        if not check_password_hash(admin.password_hash, password):
            return apology(" pass is incorect!")
        session["user_id"] = admin.id
        session["user_type"] = "admin"
        return redirect('/')


@app.route("/login_teacher", methods=["GET","POST"])
def login_teacher():
    session.clear()
    if request.method == "GET":
        redirect("/") 
    else:
        #todo implement login
        if not ((username := request.form.get("username")) and (password := request.form.get("password"))):
            return apology("user or pass is incorect!")

        session["user_id"] = ...
        session["user_type"] = "teachers"
        return redirect('/')


@app.route("/logout", methods=["GET","POST"])
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
