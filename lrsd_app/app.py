from flask import Flask , session, render_template, redirect , request
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from models import Admin, Teachers, Departments, Grade , Polycopes,OnlineCourses,SupervisionMaster,SupervisionL3,Conferences,Articles
from production import Polycope, Online_course, Master, L3, Conference, Article,Production
from db import db
from auth import login_required,login_admin
from apology import apology
from werkzeug.security import generate_password_hash
from exceptions import Password_or_username_none, Pass_user_incorrect, Erorro_in_inputs,Not_user
from users import CAdmin, Teacher
from department import Department
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
    if session["user_type"] is Admin: 
        return redirect("/admin_dashboard")
    elif session["user_type"] is Teachers:
        return redirect("/teacher_dashboard")
    else:
        return apology("you are'n allowed hire")

'''
mange db and app
'''
@app.route("/add_admin", methods=["GET", "POST"])
@login_admin
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

@app.route("/delete_admin", methods=["GET", "POST"])
@login_admin
def delete_admin():
    if request.method == "GET":
        return redirect("/")
    else:
        username = request.form.get("user_name")
        new_admin = Admin.query.filter(Admin.username == username).first()
        db.session.delete(new_admin)
        db.session.commit()
        return redirect("/")

@app.route("/add_department", methods=["GET", "POST"])
@login_admin
def add_department():
    if request.method == "GET":
        return redirect("/")
    else:
        name = request.form.get("name")
        new_department = Departments(name = name)
        db.session.add(new_department)
        db.session.commit()
        return redirect("/")
@app.route("/delete_department", methods=["GET", "POST"])
@login_admin
def delete_department():
    if request.method == "GET":
        return redirect("/")
    else:
        id = request.form.get("id")
        department = Departments.query.filter(Departments.id == id).first()
        db.session.delete(department)
        db.session.commit()
        return redirect("/")
    
    
@app.route("/add_grade", methods=["GET", "POST"])
@login_admin
def add_grade():
    if request.method == "GET":
        return redirect("/")
    else:
        grade_ = request.form.get("grade")
        grade = Grade(grade = grade_)
        db.session.add(grade)
        db.session.commit()
        return redirect("/")
    
@app.route("/delete_grade", methods=["GET", "POST"])
@login_admin
def delete_grade():
    if request.method == "GET":
        return redirect("/")
    else:
        grade_ = request.form.get("grade")
        grade = Grade.query.filter(Grade.grade == grade_).first()
        db.session.delete(grade)
        db.session.commit()
        return redirect("/")


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
    
    return render_template("dashboard.html",departments = Departments.query.all(), grades = Grade.query.all(),admins =  Admin.query.all())

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
        try:
            Teacher(par=request.form).add()
        except:
            return apology("user name all ready exist")

        return redirect("/teachers_list")

@app.route("/teachers")
@login_required
def teachers_():
    teachers = [{"id":teacher.id, "first_name":teacher.first_name, "last_name":teacher.last_name, "username": teacher.username, "department": Departments.query.filter(Departments.id == teacher.department_id).with_entities(Departments.name).first().name}
                for teacher in Teachers.query.with_entities(Teachers.id, Teachers.first_name, Teachers.last_name, Teachers.username, Teachers.department_id)]    

    return render_template("teachers.html", departments = Departments.query.all(), teachers = teachers, grades = Grade.query.all())

@app.route("/teachers_list")
@login_required
def teachers_list():
    teachers = Teachers.query.with_entities(Teachers.first_name,Teachers.last_name,Teachers.username ,Teachers.id).all()
    return render_template("teachers_list.html",departments = Departments.query.all(), teachers = teachers, grades = Grade.query.all())

    
@app.route("/delete_teacher", methods=["POST"])
@login_required
def delete_teacher():
    Teacher(par=request.form).delete()
    return redirect(request.referrer)

@app.route("/edit_teacher", methods=["POST"])
@login_required
def edit_teacher():
    try:
        Teacher(par=request.form).edit()
    except Not_user:
        return apology("username all ready exixst!")
    '''except:
        return apology("sommethin go ronge!")'''
    return redirect(request.referrer)

@app.route("/profile")
def profile():
    
    if request.args.get("user"):
        if teacher := Teacher.teacher_profile(request.args.get("user")):
            productions = Production.by_teachers(teacher["id"])
            return render_template("profile_a.html",teacher = teacher, productions = productions, edit = True) if session["user_type"] is Admin else render_template("profile.html",teacher = teacher, productions = productions, edit = True)
            
    
    return apology("something go wrowng ")


'''
 -------------------------------
        MANGE PRODUCTIONS 
-------------------------------

'''

@app.route("/productions_list")
@login_required
def productions_list():
    return render_template("production_list.html",user ="admin" if session.get("user_type") is Admin else "teacher" )

@app.route("/productions")
@login_required
def productions():
    if session.get("user_type") is Teachers:
        query =Production.by_teacher(session.get("user_id"))
    else:
        query = Production.all()
        
    return render_template("productions.html", productions = query)

@app.route("/add_production", methods=["GET","POST"])
@login_required
def add_production():
    if request.method == "GET":
        if session.get("user_type") is Admin: 
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
                    p = Polycope(request.form)
                    p.add()
                case "online_courses":
                    p = Online_course(request.form)
                    p.add()
                case "master":
                    p = Master(request.form)
                    p.add()
                case "l3":
                    p = L3(request.form)
                    p.add()
                case "conference":
                    p = Conference(request.form)
                    p.add()
                case "article":
                    p = Article(request.form)
                    p.add()
                case _:
                    return apology("semthin went rowong")
            return redirect(request.referrer)
        except Erorro_in_inputs:
            return apology("Erorro in the inputs")

@app.route("/edit_production", methods=["GET","POST"])
@login_required
def edit_production():
    if request.method == "GET":
        production = request.args.get("p") if request.args.get("p") else "polycopes"
        if request.args.get("id"):
            id = request.args.get("id") 
        else:
            raise ValueError
        return render_template("edit_production.html", production = production, id =id)
    else:
        try:
            match request.form.get("production"):
                case "polycopes":
                    Production.edit(Polycopes,request.form)
                case "online_courses":
                    Production.edit(OnlineCourses,request.form)
                case "master":
                    Production.edit(SupervisionMaster,request.form)
                case "l3":
                    Production.edit(SupervisionL3,request.form)
                case "conference":
                    Production.edit(Conferences,request.form)
                case "article":
                    Production.edit(Articles,request.form)
                case _:
                    return apology("semthin went rowong")
            return redirect(request.referrer)
        except Erorro_in_inputs:
            return apology("Erorro in the inputs")
        
@app.route("/delete_production",methods=["GET","POST"])
@login_required
def delete_production():
    
    match request.form.get("production"):
        case "polycopes":
            Production.delete(Polycopes,request.form.get("id"))
        case "online_courses":
            Production.delete(OnlineCourses,request.form.get("id"))
        case "master":
            Production.delete(SupervisionMaster,request.form.get("id"))
        case "l3":
            Production.delete(SupervisionL3,request.form.get("id"))
        case "conference":
            Production.delete(Conferences,request.form.get("id"))
        case "article":
            Production.delete(Articles,request.form.get("id"))
        case _:
            return apology("semthin went rowong")
    return redirect(request.referrer)

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
    
    return redirect("/teachers_profile")

@app.route("/teachers_profile")
@login_required
def teachers_profile():
    
    return render_template("teachers_profile.html",username = Teachers.query.filter(Teachers.id == session.get("user_id")).with_entities(Teachers.username).first().username)


'''
 -------------------------------
 *******************************

        statistic

 *******************************
-------------------------------

'''

@app.route("/statistic")
@login_required
def statistic():
    production = Production.statistic(username = request.args.get("username"), department_id= request.args.get("department"))
    teachers = Teacher.total(department_id=request.args.get("department"))
    best = Teacher.best()
    department = Department.statistic_d(department_id=request.args.get("department"))
    return render_template("statistic.html", production = production,best = best,teachers = teachers,teachers_l = Teachers.query.with_entities(Teachers.username,Teachers.first_name,Teachers.last_name),department_l =Departments.query.all() ,departments = department,f_t =request.args.get("username") , f_d = department[0]["name"] if request.args.get("department") else None , user ="admin" if session.get("user_type") is Admin else "teacher")


'''
guest
'''
@app.route("/guest")
def guest():
    return render_template("guest.html", teachers = Teachers.query.all())


@app.route("/gueststat")
def gueststat():
    production = Production.statistic(username = request.args.get("username"), department_id= request.args.get("department"))
    teachers = Teacher.total(department_id=request.args.get("department"))
    best = Teacher.best()
    department = Department.statistic_d(department_id=request.args.get("department"))
    return render_template("gueststat.html", production = production,best = best,teachers = teachers,teachers_l = Teachers.query.with_entities(Teachers.username,Teachers.first_name,Teachers.last_name),department_l =Departments.query.all() ,departments = department,f_t =request.args.get("username") , f_d = department[0]["name"] if request.args.get("department") else None , user ="admin" if session.get("user_type") is Admin else "teacher")


@app.route("/guest_profile")
def guest_profile():
    
    if request.args.get("user"):
        if teacher := Teacher.teacher_profile(request.args.get("user")):
            productions = Production.by_teachers(teacher["id"])
            return render_template("guest_profile.html",teacher = teacher, productions = productions, edit = False)
    
    return apology("something go wrowng ")




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
            CAdmin(user_name=request.form.get("username"),password=request.form.get("password")).login()
        except Password_or_username_none or Pass_user_incorrect as e:
            return apology(e.error["msg"])

        return redirect('/')

@app.route("/login_teacher", methods=["GET","POST"])
def login_teacher():
    session.clear()
    if request.method == "GET":
        return redirect("/") 
    else:
        try:
            Teacher(user_name=request.form.get("username"),password=request.form.get("password")).login()
        except Password_or_username_none or Pass_user_incorrect as e:
            return apology(e.error["msg"])
        return redirect('/')


@app.route("/logout", methods=["GET","POST"])
def logout():
    session.clear()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
