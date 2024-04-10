from flask import Flask , session, render_template, redirect , request
from flask_session import Session
from flask_mysqldb import MySQL
from auth import login_required
from apology import apology
from werkzeug.security import check_password_hash, generate_password_hash
# app config
app = Flask(__name__)

# session config 
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# db config 
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "aymen"
app.config["MYSQL_DB"] = "lrsd"
mysql = MySQL(app)  

@app.route('/')
@login_required
def index():
    return render_template("index.html")



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
            return apology("user or pass is incorect!")
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM admin WHERE username = %s", (username,))

        if not (user := cur.fetchone()):
            return apology("user or pass is incorect!")
        if not(check_password_hash(user[3], password)):
                return apology("user or pass is incorect!")
        session["user_id"] = user[0]
        session["user_type"] = "admin"
        mysql.connection.commit()  # Commit the transaction
        cur.close()
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
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM teachers WHERE username = %s", (username,))

        if not (user := cur.fetchone()):
            return apology("user or pass is incorect!")
        if not(check_password_hash(user[3], password)):
                return apology("user or pass is incorect!")
        session["user_id"] = user[0]
        session["user_type"] = "teachers"
        mysql.connection.commit()  # Commit the transaction
        cur.close()
        return redirect('/')


@app.route("/logout", methods=["GET","POST"])
def logout():
    ...