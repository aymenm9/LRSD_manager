from models import Teachers, Polycopes, OnlineCourses , SupervisionMaster, SupervisionL3, Conferences, Articles, Intervention, ConferenceAssistants,Coauthor
from abc import ABC,abstractmethod
from exceptions import Not_user, Erorro_in_inputs
from db import db

class Production(ABC):
    def __init__(self, par : dict = None, production = None):
        self.par = par
        self.production = production if production else None

    def add(self):
        #get teacher 
        if not (Teachers.query.filter(Teachers.id == self.par.get("teacher_id")).first()):
            raise Not_user({"msg": "teacher don't exist"})
        #selef method 
        self.add_self()
        #commit to db
        db.session.add(self.production)
        db.session.commit()
    
    @staticmethod
    def delete_all(teacher_id):
        for production in  Production.__subclasses__():
            production.delete(teacher_id)


    @abstractmethod
    def add_self(self):
        pass
    @staticmethod
    @abstractmethod
    def delete(teacher_id):
        pass

class Polycope(Production):
    def __init__(self,par: dict, production=None):
        super().__init__(par, production)
    
    def add_self(self):
        try:
            self.production = Polycopes(title = self.par.get("title"), pages = self.par.get("pages"), date =self.par.get("date"), type = self.par.get("type"), teacher_id =self.par.get("teacher_id"))
        except:
            raise Erorro_in_inputs
    
    @staticmethod
    def delete_all(teacher_id):
        for pol in Polycopes.query.filter_by(teacher_id = teacher_id).all():
            db.session.delete(pol)
        db.session.commit()
    
class Online_course(Production):
    def __init__(self,par: dict, production=None):
        super().__init__(par, production)

    def add_self(self):
        try:
            self.production = OnlineCourses(title = self.par.get("title"), date =self.par.get("date"), url = self.par.get("url") ,teacher_id =self.par.get("teacher_id"))
        except:
            raise Erorro_in_inputs
        
    @staticmethod
    def delete_all(teacher_id):
        for pol in OnlineCourses.query.filter_by(teacher_id = teacher_id).all():
            db.session.delete(pol)
        db.session.commit()

class Master(Production):
    def __init__(self, par: dict, production=None):
        super().__init__(par, production)

    def add_self(self):
        try:
            self.production = SupervisionMaster(subject = self.par.get("subject"), binome_1 = self.par.get("binome_1"), binome_2 = self.par.get("binome_2") if self.par.get("binome_2") else None, graduation_date = self.par.get("graduation_date")  , teacher_id =self.par.get("teacher_id"))
        except:
            raise Erorro_in_inputs
        
    @staticmethod
    def delete_all(teacher_id):
        for pol in SupervisionMaster.query.filter_by(teacher_id = teacher_id).all():
            db.session.delete(pol)
        db.session.commit()

class L3(Production):
    def __init__(self, par: dict, production=None):
        super().__init__(par, production)

    def add_self(self):
        try:
            self.production = SupervisionL3(subject = self.par.get("subject"), binome_1 = self.par.get("binome_1"), binome_2 = self.par.get("binome_2") if self.par.get("binome_2") else None , teacher_id =self.par.get("teacher_id"))
        except:
            raise Erorro_in_inputs
    
    @staticmethod
    def delete_all(teacher_id):
        for pol in SupervisionL3.query.filter_by(teacher_id = teacher_id).all():
            db.session.delete(pol)
        db.session.commit()

class Extra(ABC):
    def __init__(self, names, production):
        self.production = production
        if names:
            for name in names.split(","):
                extra = self.add_self(name.strip())
                db.session.add(extra)
                db.session.commit()

    @abstractmethod
    def add_self(self, name):
        pass

class Assistants (Extra):
    def __init__(self,  names,production):
        super().__init__( names,production)
    def add_self(self,name):
        return ConferenceAssistants(conference_id = self.production , assistant_name = name)

class Interventions (Extra):
    def __init__(self,  names,production):
        super().__init__( names,production)
    def add_self(self,name):
        return Intervention(conference_id = self.production , intervention = name)

class Coauthors (Extra):
    def __init__(self,  names,production):
        super().__init__( names,production)
        
    def add_self(self,name):
        return Coauthor(article_id = self.production , name = name)

class Conference(Production):
    def __init__(self,   par: dict, production=None):
        super().__init__(  par, production)
    def add(self):
        super().add()
        self.add_extra()
    def add_extra(self):
        Assistants( self.par.get("assistants"),self.production.id)
        Interventions(self.par.get("interventions"),self.production.id)
    def add_self(self):
        try:
            self.production = Conferences(name = self.par.get("name"), place = self.par.get("place"), date =self.par.get("date"), teacher_id =self.par.get("teacher_id"))
        except:
           raise Erorro_in_inputs

class Article(Production):
    def __init__(self,   par: dict, production=None):
        super().__init__(  par, production)
    
    def add(self):
        super().add()
        self.add_extra()

    def add_extra(self):
        Coauthors(self.par.get("coauthors"),self.production.id)

    def add_self(self):
        try:
            self.production = Articles(title = self.par.get("title") , pages = self.par.get("pages"), journal=self.par.get("journal"), date = self.par.get("date"), teacher_id =self.par.get("teacher_id"))
        except:
            raise Erorro_in_inputs