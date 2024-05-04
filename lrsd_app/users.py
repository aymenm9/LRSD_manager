from models import Teachers, Admin, Polycopes, OnlineCourses , SupervisionMaster, SupervisionL3, Conferences, Articles, Intervention, ConferenceAssistants,Coauthor
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
    def __init__(self, *, id=None, user_name=None, password=None) -> None:
        super().__init__(id=id, user_name=user_name, password=password)
    
    def myclass(self):
        return Teachers