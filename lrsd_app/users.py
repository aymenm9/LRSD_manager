from models import Teachers, Admin,Departments
from abc import ABC,abstractmethod
from exceptions import Not_user, Erorro_in_inputs, Password_or_username_none, Pass_user_incorrect
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from db import db

class User(ABC):
    def __init__(self,*,id = None, user_name = None, password = None) -> None:
        self.id = id
        self.user_name = user_name
        self.password = password
        self.user = None
        self._class = self.myclass()

    def login(self):
        if not (self.user_name and self.password):
            raise Password_or_username_none()
        self.user = self._class.query.filter_by(username=self.user_name).first()
        if not self.user:
            raise Pass_user_incorrect({"username": True, "msg": "username is incorrect!"})

        if not check_password_hash(self.user.password_hash, self.password):
            raise Pass_user_incorrect({"password": True , "msg":"password is incorect!"})
        session["user_id"] = self.user.id
        session["user_type"] = self._class
        
    @abstractmethod
    def myclass(self):
        pass

class CAdmin(User):
    def __init__(self, *, id=None, user_name=None, password=None) -> None:
        super().__init__(id=id, user_name=user_name, password=password)
    
    def myclass(self):
        return Admin
    
class Teacher(User):
    def __init__(self, *, id=None, user_name=None, password=None, par : dict = None) -> None:
        super().__init__(id=id, user_name=user_name, password=password)
        self.par = par
    
    def myclass(self):
        return Teachers
    
    def add(self):
        if not (self.par.get("username") and self.unique_username() and self.par.get("password") and self.par.get("department")) :
            raise Not_user
        self.teacher = Teachers(username = self.par.get("username") , password_hash = generate_password_hash(self.par.get("password")), department_id = self.par.get("department"))
        if self.par.get("img"):
            self.teacher.img = self.par.get("img")
        if self.par.get("first_name"):
            self.teacher.first_name = self.par.get("first_name")
        if self.par.get("last_name"):
            self.teacher.last_name = self.par.get("last_name")
        if self.par.get("grade"):
            self.teacher.grade = self.par.get("grade")
        if self.par.get("email"):
            self.teacher.email = self.par.get("email")
        db.session.add(self.teacher)
        db.session.commit()
    def delete(self):
        self.teacher = Teachers.query.filter_by(id = self.par.get("id")).first()
        db.session.delete(self.teacher)
        db.session.commit()

    def edit(self):
        self.teacher = Teachers.query.filter_by(id = self.par.get("id")).first()
        if self.par.get("password"):
            self.teacher.password = self.par.get("password")
        if self.par.get("username") :
            if not self.unique_username():
                raise Not_user
            self.teacher.username = self.par.get("username")
        if self.par.get("department"):
            self.teacher.department_id = self.par.get("department")
        if self.par.get("first_name"):
            self.teacher.first_name = self.par.get("first_name")
        if self.par.get("last_name"):
            self.teacher.last_name = self.par.get("last_name")
        if self.par.get("grade"):
            self.teacher.grade = self.par.get("grade")
        if self.par.get("email"):
            self.teacher.email = self.par.get("email")
        db.session.commit()
    @staticmethod
    def teacher_profile(user_name):
        teacher = Teachers.query.with_entities(Teachers.id, Teachers.first_name, Teachers.last_name, Teachers.grade, Teachers.department_id, Teachers.email).filter(Teachers.username == user_name).first()
        return {"id": teacher.id,"full_name": teacher.first_name + " " + teacher.last_name, "grade": teacher.grade, "email": teacher.email, "department": Departments.query.filter(Departments.id == teacher.department_id).with_entities(Departments.name).first().name} if teacher else None
                
    def unique_username(self):
        if Teachers.query.filter_by(username = self.par.get("username")).all():
            return False
        else:
            return True
            