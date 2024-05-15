from models import Teachers, Polycopes, OnlineCourses , SupervisionMaster, SupervisionL3, Conferences, Articles, Intervention, ConferenceAssistants,Coauthor
from abc import ABC,abstractmethod
from exceptions import Not_user, Erorro_in_inputs
from sqlalchemy import select
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
    
    @abstractmethod
    def add_self(self):
        pass

    @abstractmethod
    def get_all():
        pass
    @staticmethod
    def edit(object,par):
        production = object.query.filter(object.id == par.get("production_id")).first()
        if production:
            if par.get("title"): # For Polycopes or onlineCouse or Articals class 
                production.title = par.get("title")
            elif par.get("date"):  # For ... class 
                production.pages = par.get("date")
            elif par.get("pages"):  # For Polycopes class 
                production.pages = par.get("pages")
            elif par.get("url"):  # For OnlineCourses class
                production.url = par.get("url")
            elif par.get("binome_2"):  # For SupervisionL3 or SupervisionMaster class
                production.binome_2 = par.get("binome_2")
            elif par.get("graduation_date"):  # Only for SupervisionMaster class
                production.graduation_date = par.get("graduation_date")
            elif par.get("name"):  # For Conferences class
                production.name = par.get("name")
            elif par.get("place"):  # For Conferences class
                production.place = par.get("place")
            elif par.get("journal"):  # Unique attribute for Articles class
                production.journal = par.get("journal")
            elif par.get("assistants"):  # For Conferences class
                Assistants.delele(production.id)
                Assistants(par.get("assistants"),production.id)
            elif par.get("interventions"):  # For Conferences class
                Interventions.delele(production.id)
                Interventions(par.get("interventions"),production.id)
            elif par.get("coauthors"):  # For Conferences class
                Coauthors.delele(production.id)
                Coauthors(par.get("coauthors"),production.id)

        db.session.commit()

    @staticmethod
    def delete(object,id):
        production = object.query.filter(object.id == id).first()
        db.session.delete(production)
        db.session.commit()
    @staticmethod
    def by_teacher(id):
        productions = []
        
        for inst in Production.__subclasses__():
            prods = inst.get_all_t(id)
            for prod in prods:
                teacher = Teachers.query.filter(Teachers.id == prod["teacher"]).with_entities(Teachers.first_name, Teachers.last_name).first()
                prod["teacher"] = teacher.first_name + " "+teacher.last_name
                productions.append(prod)
        return  productions
    @staticmethod
    def by_teachers(id):
        productions = []
        exclude_fields = {'teacher_id', 'id'}
        for inst in Production.__subclasses__():
            prods = inst.type().query.all()
            for prod in prods:
                prod_dict={}
                for field in prod.__table__.columns.keys():
                    if field not in exclude_fields:
                        prod_dict[field.replace('_', ' ')] = getattr(prod, field)
                prod_dict["types"]= inst.type(True)
                productions.append(prod_dict)
        return  productions

    @staticmethod
    def statistic(*,username = None, department_id = None):
        statistic={
            "total": 0,
            "scientist":0,
            "pedagogic":0,
        }
        if username:
            teacher= Teachers.query.filter(Teachers.username == username).with_entities(Teachers.id).first()
            teacher_id = teacher.id
        else:
            teacher_id= None
        for inst in Production.__subclasses__():
            stat = inst.type().query.with_entities(inst.type().id)
            if teacher_id:
                stat = stat.filter(inst.type().teacher_id == teacher_id)
            if department_id:
                teachers = Teachers.query.with_entities(Teachers.id).filter(Teachers.department_id == department_id).subquery()
                teachers_select = select(teachers)
                stat = stat.filter(inst.type().teacher_id.in_(teachers_select))
            x = stat.count()
            statistic[inst.type(True)] = x
            statistic["total"] = statistic["total"] + x
            if inst.type(True) in ["Conference","Article"]:
                statistic["scientist"] = statistic["scientist"] + x
            else:
                statistic["pedagogic"] = statistic["pedagogic"] + x

        return statistic


    @staticmethod
    def all():
        productions = []
        for inst in Production.__subclasses__():

            prods = inst.get_all()
            for prod in prods:
                teacher = Teachers.query.filter(Teachers.id == prod["teacher"]).with_entities(Teachers.first_name, Teachers.last_name,Teachers.username).first()
                prod["teacher"] =teacher.first_name + " "+teacher.last_name
                productions.append(prod)
        return  productions


class Polycope(Production):
    def __init__(self,par: dict, production=None):
        super().__init__(par, production)
    
    def add_self(self):
        try:
            self.production = Polycopes(title = self.par.get("title"), pages = self.par.get("pages"), date =self.par.get("date"), type = self.par.get("type"), teacher_id =self.par.get("teacher_id"))
        except:
            raise Erorro_in_inputs
    @staticmethod
    def get_all():
        return [{"id": col.id, "title": col.title,"date":col.date,"teacher":col.teacher_id,"type":"polycopes"}
                 for col in Polycopes.query.with_entities(Polycopes.id, Polycopes.title, Polycopes.date, Polycopes.teacher_id)]
    @staticmethod
    def get_all_t(id):
        return [{"id": col.id, "title": col.title,"date":col.date,"teacher":col.teacher_id,"type":"polycopes"}
                 for col in Polycopes.query.filter(Polycopes.teacher_id == id).with_entities(Polycopes.id, Polycopes.title, Polycopes.date, Polycopes.teacher_id)]
    
    @staticmethod
    def type(st = None):
        return "Polycope" if st else Polycopes
    
class Online_course(Production):
    def __init__(self,par: dict, production=None):
        super().__init__(par, production)

    def add_self(self):
        try:
            self.production = OnlineCourses(title = self.par.get("title"), date =self.par.get("date"), url = self.par.get("url") ,teacher_id =self.par.get("teacher_id"))
        except:
            raise Erorro_in_inputs

    @staticmethod
    def get_all():
        
        return [{"id": col.id, "title": col.title,"date":col.date,"teacher":col.teacher_id,"type":"online_courses"}
            for col in OnlineCourses.query.with_entities(OnlineCourses.id ,OnlineCourses.title,OnlineCourses.date,OnlineCourses.teacher_id)]     
    @staticmethod
    def get_all_t(id):
        return [{"id": col.id, "title": col.title,"date":col.date,"teacher":col.teacher_id,"type":"online_courses"}
            for col in OnlineCourses.query.with_entities(OnlineCourses.id ,OnlineCourses.title,OnlineCourses.date,OnlineCourses.teacher_id).filter(OnlineCourses.teacher_id == id)]    
    @staticmethod
    def type(st = None):
        return "Online course" if st else OnlineCourses


class Master(Production):
    def __init__(self, par: dict, production=None):
        super().__init__(par, production)

    def add_self(self):
        try:
            self.production = SupervisionMaster(subject = self.par.get("subject"), binome_1 = self.par.get("binome_1"), binome_2 = self.par.get("binome_2") if self.par.get("binome_2") else None, graduation_date = self.par.get("graduation_date")  , teacher_id =self.par.get("teacher_id"))
        except:
            raise Erorro_in_inputs
        
    @staticmethod
    def get_all():
        return [{"id": col.id, "title": col.subject,"date":col.graduation_date,"teacher":col.teacher_id,"type":"master"}
            for col in SupervisionMaster.query.with_entities(SupervisionMaster.id ,SupervisionMaster.subject,SupervisionMaster.graduation_date,SupervisionMaster.teacher_id)] 
    @staticmethod
    def get_all_t(id):
        return [{"id": col.id, "title": col.subject,"date":col.graduation_date,"teacher":col.teacher_id,"type":"master"}
            for col in SupervisionMaster.query.with_entities(SupervisionMaster.id ,SupervisionMaster.subject,SupervisionMaster.graduation_date,SupervisionMaster.teacher_id).filter(SupervisionMaster.teacher_id == id)]     

    @staticmethod
    def type(st = None):
        return "Supervision Master" if st else SupervisionMaster

class L3(Production):
    def __init__(self, par: dict, production=None):
        super().__init__(par, production)

    def add_self(self):
        try:
            self.production = SupervisionL3(subject = self.par.get("subject"), binome_1 = self.par.get("binome_1"), binome_2 = self.par.get("binome_2") if self.par.get("binome_2") else None , teacher_id =self.par.get("teacher_id"))
        except:
            raise Erorro_in_inputs
    
    @staticmethod
    def get_all():
        return [{"id": col.id, "title": col.subject,"date":None,"teacher":col.teacher_id,"type":"l3"}
            for col in SupervisionL3.query.with_entities(SupervisionL3.id ,SupervisionL3.subject, SupervisionL3.teacher_id)]   
    @staticmethod
    def get_all_t(id):
        return [{"id": col.id, "title": col.subject,"date":None,"teacher":col.teacher_id,"type":"l3"}
            for col in SupervisionL3.query.with_entities(SupervisionL3.id ,SupervisionL3.subject, SupervisionL3.teacher_id).filter(SupervisionL3.teacher_id == id)]   
    @staticmethod
    def type(st = None):
        return "Supervision L3" if st else SupervisionL3

class Extra(ABC):
    def __init__(self, names, production):
        self.production = production
        if names:
            for name in names.split(","):
                extra = self.add_self(name.strip())
                db.session.add(extra)
                db.session.commit()
    @staticmethod
    @abstractmethod
    def delete(id):
        pass


    @abstractmethod
    def add_self(self, name):
        pass

class Assistants (Extra):
    def __init__(self,  names,production):
        super().__init__( names,production)
    def add_self(self,name):
        return ConferenceAssistants(conference_id = self.production , assistant_name = name)

    @staticmethod
    def delele(id):
        for extra in ConferenceAssistants.query.filter(ConferenceAssistants.conference_id == id).all():
            db.session.delete(extra)
            db.session.commit()


class Interventions (Extra):
    def __init__(self,  names,production):
        super().__init__( names,production)
    def add_self(self,name):
        return Intervention(conference_id = self.production , intervention = name)
    @staticmethod
    def delele(id):
        for extra in Intervention.query.filter(Intervention.conference_id == id).all():
            db.session.delete(extra)
            db.session.commit()

class Coauthors (Extra):
    def __init__(self,  names,production):
        super().__init__( names,production)
        
    def add_self(self,name):
        return Coauthor(article_id = self.production , name = name)

    @staticmethod
    def delele(id):
        for extra in Coauthor.query.filter(Coauthor.article_id == id).all():
            db.session.delete(extra)
            db.session.commit()


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
        
    @staticmethod
    def get_all():
        return [{"id": col.id, "title": col.name,"date":col.date,"teacher":col.teacher_id,"type":"conference" }
            for col in Conferences.query.with_entities(Conferences.id ,Conferences.name,Conferences.date,Conferences.teacher_id)]
    @staticmethod
    def get_all_t(id):
        return [{"id": col.id, "title": col.name,"date":col.date,"teacher":col.teacher_id,"type":"conference" }
            for col in Conferences.query.with_entities(Conferences.id ,Conferences.name,Conferences.date,Conferences.teacher_id).filter(Conferences.teacher_id == id)]    

    @staticmethod
    def type(st = None):
        return "Conference" if st else Conferences
     
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
        
    @staticmethod
    @abstractmethod
    def get_all():
        return [{"id": col.id, "title": col.title,"date":col.date,"teacher":col.teacher_id,"type": "article"}
            for col in Articles.query.with_entities(Articles.id ,Articles.title,Articles.date,Articles.teacher_id)] 
    @staticmethod
    def get_all_t(id):
        return [{"id": col.id, "title": col.title,"date":col.date,"teacher":col.teacher_id,"type": "article"}
            for col in Articles.query.with_entities(Articles.id ,Articles.title,Articles.date,Articles.teacher_id).filter(Articles.teacher_id == id)]    

    @staticmethod
    def type(st = None):
        return "Article" if st else Articles