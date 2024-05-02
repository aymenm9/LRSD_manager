from models import Teachers, Polycopes
from abc import ABC,abstractmethod
from exceptions import Not_user, Erorro_in_inputs

class Production(ABC):
    def __init__(self, db, par : dict, production = None):
        self.db = db
        self.par = par
        self.production = production if production else None

    def add(self):
        #get teacher 
        if not (Teachers.query.filter(Teachers.id == self.par.get("teacher_id")).first()):
            raise Not_user({"msg": "teacher don't exist"})
        #selef method 
        self.add_self()
        #commit to db
        self.db.session.add(self.production)
        self.db.session.commit()

    @abstractmethod
    def add_self(self):
        pass

class MPolycopes(Production):
    def __init__(self, db, par: dict, production=None):
        super().__init__(db, par, production)
    
    def add_self(self):
        try:
            self.production = Polycopes(title = self.par.get("title"), pages = self.par.get("pages") , date =self.par.get("date"), type = self.par.get("type"), teacher_id =self.par.get("teacher_id"))
        except:
            raise Erorro_in_inputs

class Online_courses(Production):
    def __init__(self, par: dict, production=None):
        super().__init__(par, production)

class Master(Production):
    def __init__(self, par: dict, production=None):
        super().__init__(par, production)
class L3(Production):
    def __init__(self, par: dict, production=None):
        super().__init__(par, production)

class Conference(Production):
    def __init__(self, par: dict, production=None):
        super().__init__(par, production)

class Article(Production):
    def __init__(self, par: dict, production=None):
        super().__init__(par, production)