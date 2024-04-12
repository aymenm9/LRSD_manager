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

class Teachers(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable= False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(255))
    password_hash = Column(String(255), nullable=False)
    mark = Column(Float)
    grade = Column(String(255))
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)

    # Relationship definition (optional)
    department = db.relationship('Departments', backref='teachers')