from db import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Enum
from abc import ABC

class Admin(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255))
    password_hash = Column(String(255), nullable=False)

class Departments(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)

class Grade(db.Model):
    grade = Column(String(50), nullable=False, primary_key=True)

class Teachers(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable= False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(255))
    password_hash = Column(String(255), nullable=False)
    mark = Column(Float)
    grade = Column(String(255))
    department_id = Column(Integer, ForeignKey(Departments.id), nullable=False)

class Polycopes(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255),nullable=False)
    pages= Column(Integer,nullable=False)
    date = Column(Date,nullable=False)
    type = Column(Enum('td', 'tp', 'cour'),nullable=False)
    teacher_id = Column(Integer,ForeignKey(Teachers.id),nullable=False)

class OnlineCourses(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255),nullable=False)
    url = Column(String(255),nullable=False)
    date = Column(Date,nullable=False)
    teacher_id = Column(Integer,ForeignKey(Teachers.id),nullable=False)

class SupervisionL3(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    subject = Column(String(255), nullable=False)
    binome_1 = Column(String(255), nullable=False)
    binome_2 = Column(String(255))
    teacher_id = Column(Integer,ForeignKey(Teachers.id),nullable=False)

class SupervisionMaster(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    subject = Column(String(255), nullable=False)
    binome_1 = Column(String(255), nullable=False)
    binome_2 = Column(String(255))
    graduation_date = Column(Date, nullable=False)
    teacher_id = Column(Integer,ForeignKey(Teachers.id),nullable=False)

class Conferences(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    place = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)
    teacher_id = Column(Integer,ForeignKey(Teachers.id),nullable=False)

class ConferenceAssistants(db.Model):
    conference_id = Column(Integer, ForeignKey(Conferences.id), primary_key=True, nullable=False)
    assistant_name = Column(String(255), primary_key=True, nullable=False)


class Intervention(db.Model):
    conference_id = Column(Integer, ForeignKey('Conferences.id'), primary_key=True, nullable=False)
    intervention = Column(String(255))

class Articles(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)
    pages = Column(Integer)
    journal = Column(String(255))
    teacher_id = Column(Integer,ForeignKey(Teachers.id),nullable=False)

class Coauthor(db.Model):
    article_id = Column(Integer, ForeignKey(Articles.id), primary_key=True, nullable=False)
    name = Column(String(255), primary_key=True, nullable=False)