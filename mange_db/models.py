from db import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey
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
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(255))
    password_hash = Column(String(255), nullable=False)
    mark = Column(Float, nullable=False)
    grade = Column(String(255), nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'))

    # Relationship definition (optional)
    department = db.relationship('Departments', backref='teachers')