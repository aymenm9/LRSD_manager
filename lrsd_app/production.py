from models import Teachers, Polycopes, OnlineCourses , SupervisionMaster, SupervisionL3, Conferences, Articles, Intervention, ConferenceAssistants,Coauthor
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

class Polycope(Production):
    def __init__(self, db, par: dict, production=None):
        super().__init__(db, par, production)
    
    def add_self(self):
        try:
            self.production = Polycopes(title = self.par.get("title"), pages = self.par.get("pages"), date =self.par.get("date"), type = self.par.get("type"), teacher_id =self.par.get("teacher_id"))
        except:
            raise Erorro_in_inputs

class Online_courses(Production):
    def __init__(self, db, par: dict, production=None):
        super().__init__(db, par, production)

    def add_self(self):
        try:
            self.production = OnlineCourses(title = self.par.get("title"), date =self.par.get("date"), url = self.par.get("url") ,teacher_id =self.par.get("teacher_id"))
        except:
            raise Erorro_in_inputs 

class Master(Production):
    def __init__(self, db, par: dict, production=None):
        super().__init__(db, par, production)

    def add_self(self):
        try:
            self.production = SupervisionMaster(subject = self.par.get("subject"), binome_1 = self.par.get("binome_1"), binome_2 = self.par.get("binome_2") if self.par.get("binome_2") else None, graduation_date = self.par.get("graduation_date")  , teacher_id =self.par.get("teacher_id"))
        except:
            raise Erorro_in_inputs
class L3(Production):
    def __init__(self, db, par: dict, production=None):
        super().__init__(db, par, production)

    def add_self(self):
        try:
            self.production = SupervisionL3(subject = self.par.get("subject"), binome_1 = self.par.get("binome_1"), binome_2 = self.par.get("binome_2") if self.par.get("binome_2") else None , teacher_id =self.par.get("teacher_id"))
        except:
            raise Erorro_in_inputs

class Extra(ABC):
    def __init__(self,db, names, production):
        self.db = db
        self.production = production
        if name:
            for name in names.split(","):
                extra = self.add_self(name.strip())
                self.db.session.add(extra)
                self.db.session.commit()

    @abstractmethod
    def add_self(self, name):
        pass

class Assistants (Extra):
    def __init__(self,db, names,production):
        super().__init__(db,names,production)
    def add_self(self,name):
        return ConferenceAssistants(conference_id = self.production.id , assistant_name = name)

class Interventions (Extra):
    def __init__(self,db, names,production):
        super().__init__(db,names,production)
    def add_self(self,name):
        return Intervention(conference_id = self.production.id , intervention = name)

class Coauthors (Extra):
    def __init__(self,db, names,production):
        super().__init__(db,names,production)
    def add_self(self,name):
        return Coauthor(article_id = self.production.id , name = name)

class Conference(Production):
    def __init__(self, db, par: dict, production=None):
        super().__init__(db, par, production)

    def add_self(self):
        try:
            self.production = Conferences(name = self.par.get("name"), place = self.par.get("place"), date =self.par.get("date"), teacher_id =self.par.get("teacher_id"))
            Assistants(self.db, self.par.get("assistants"),self.production)
            Interventions(self.db, self.par.get("interventions"),self.production)
                
        except:
            raise Erorro_in_inputs

class Article(Production):
    def __init__(self, db, par: dict, production=None):
        super().__init__(db, par, production)
    def add_self(self):
        try:
            self.production = Articles(title = self.par.get("title") , pages = self.par.get("pages"),date =self.par.get("journal"), journal = self.par.get("date"), teacher_id =self.par.get("teacher_id"))
            Coauthor(self.db, self.par.get("coauthors"),self.production)
        except:
            raise Erorro_in_inputs