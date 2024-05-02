from flask import Flask , session, render_template, redirect , request, jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from models import Admin, Teachers, Departments, Grade , Polycopes
from production import MPolycopes
from db import db
from auth import login_required, login_u, unique_username
from apology import apology
from werkzeug.security import check_password_hash, generate_password_hash
from exceptions import Password_or_username_none, Pass_user_incorrect, Erorro_in_inputs
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
        return redirect("/teacher_dashboard")
         
'''
 -------------------------------
 *******************************

        ADMIN  PART

 *******************************
-------------------------------

'''

@app.route("/admin_dashboard")
@login_required
def admin_dashboard():
    
    return render_template("admin_dashboard.html")

'''
 -------------------------------
        MANGE TEACHERS 
-------------------------------

'''

@app.route("/add_teacher", methods=["GET","POST"])
@login_required
def add_teacher():
    if request.method == "GET":
        redirect("/")
    else:
        if not((username := request.form.get("username")) and (password := request.form.get("password")) and (department := request.form.get("department"))):
            return apology("one is blank")
        if not unique_username(username):
            return apology("user name all ready existing! ")
        teacher = Teachers(username = username, password_hash = generate_password_hash(password), department_id = department)
        if first_name := request.form.get("first_name"):
            teacher.first_name = first_name
        if last_name := request.form.get("last_name"):
            teacher.last_name = last_name
        if grade := request.form.get("grade"):
            teacher.grade = grade
        if email := request.form.get("email"):
            teacher.email = email
        
        db.session.add(teacher)
        db.session.commit()
        return redirect("/teachers_list")

@app.route("/teachers")
@login_required
def teachers_():
    if l := request.args.get("l"):
        teachers = [{"id":teacher.id, "first_name":teacher.first_name, "last_name":teacher.last_name} 
            for teacher in Teachers.query.with_entities(Teachers.id, Teachers.first_name, Teachers.last_name).limit(l)] 
    elif q := request.args.get("q"):
        teachers = [{"id":teacher.id, "first_name":teacher.first_name, "last_name":teacher.last_name, "username": teacher.username} 
                for teacher in Teachers.query.filter((Teachers.first_name + " " +Teachers.last_name).like(f"%{q}%") + Teachers.username.like(f"%{q}%") + (Teachers.last_name + " " + Teachers.first_name).like(f"%{q}%")).with_entities(Teachers.id, Teachers.username, Teachers.first_name, Teachers.last_name)]
    else:    
        teachers = [{"id":teacher.id, "first_name":teacher.first_name, "last_name":teacher.last_name} 
                for teacher in Teachers.query.with_entities(Teachers.id, Teachers.first_name, Teachers.last_name)]
    return render_template("teachers.html", departments = Departments.query.all(), teachers = teachers, grades = Grade.query.all())

@app.route("/teachers_list")
@login_required
def teachers_list():
    teachers = Teachers.query.with_entities(Teachers.first_name,Teachers.last_name,Teachers.username ,Teachers.id).all()
    return render_template("teachers_list.html",departments = Departments.query.all(), teachers = teachers, grades = Grade.query.all())

    
@app.route("/delete_teacher", methods=["POST"])
@login_required
def delete_teacher():
    teacher = Teachers.query.filter_by(id = request.form.get("id")).first()
    db.session.delete(teacher)
    db.session.commit()
    return redirect(request.referrer)

@app.route("/edit_teacher", methods=["POST"])
@login_required
def edit_teacher():
    teacher = Teachers.query.filter_by(id = request.form.get("id")).first()
    if password := request.form.get("password"):
        teacher.password = password
    if username := request.form.get("username") :
        if not unique_username(username):
            return apology("user name all ready existing! ")
        teacher.username = username
    if department := request.form.get("department"):
        teacher.department_id = department
    if first_name := request.form.get("first_name"):
        teacher.first_name = first_name
    if last_name := request.form.get("last_name"):
        teacher.last_name = last_name
    if grade := request.form.get("grade"):
        teacher.grade = grade
    if email := request.form.get("email"):
        teacher.email = email
    db.session.commit()
    return redirect(request.referrer)


'''
 -------------------------------
        MANGE PRODUCTIONS 
-------------------------------

'''

@app.route("/productions_list")
@login_required
def productions_list():
    return render_template("production_list.html")


@app.route("/add_production", methods=["GET","POST"])
@login_required
def add_production():
    if request.method == "GET":
        if session.get("user_type") == "admin": 
           teachers = Teachers.query.with_entities( Teachers.id, Teachers.first_name,Teachers.last_name,Teachers.username).all()
           id = None
        else:
            teachers = None
            id = session.get("user_id")
        
        prod = request.args.get("p") if request.args.get("p") else "polycopes"
        return render_template("add_production.html", production = prod, teachers = teachers if teachers else None , id = id if id else None)
    else:
        try:
            match request.form.get("production"):
                case "polycopes":
                    p = MPolycopes(db,request.form)
                    p.add()
                case "online_courses":
                    ...
                case "master":
                    ...
                case "l3":
                    ...
                case "conference":
                    ...
                case "article":
                    ...
                case _:
                    return apology("semthin went rowong")
            return redirect(request.referrer)
        except Erorro_in_inputs:
            return apology("Erorro in the inputs")

'''
 -------------------------------
 *******************************

        TEACHER PART

 *******************************
-------------------------------

'''

@app.route("/teacher_dashboard")
@login_required
def teacher_dashboard():
    
    return render_template("teacher_dashboard.html")

'''
login / logout

'''
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
