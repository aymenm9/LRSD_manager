from models import Teachers
from abc import ABC,abstractmethod
from db import db
from exceptions import not_user

class production(ABC):
    def __init__(self, objct, par : dict, production = None):
        self.db = db
        self.par = par
        self.objct = objct
        self.production = production if production else None

    def add(self):
        #get teacher 
        if teacher := Teachers.query.filter_by(id = self.par["teacher_id"]).first():
            self.par["teacher"] = teacher
        else:
            raise not_user({"msg": "teacher don't exist"})
        #selef method 
        self.add_self()
        #commit to db
        db.session.add(self.production)
        db.session.commit()

    @abstractmethod
    def add_self(self):
        pass

def polycopes(request):
    ...

def online_courses(request):
    ...

def master(request):
    ...
def l3(request):
    ...

def conference(request):
    ...

def article(request):
    ...
