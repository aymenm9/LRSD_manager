from db import db
from production import Production
from models import Teachers,Departments
from users import Teacher
from abc import ABC,abstractmethod
class Department:
    @staticmethod
    def statistic_d(*,department_id=None):
        departments = Departments.query
        if department_id:
            departments = departments.filter(Departments.id == department_id)
        statistic=[]
        for department in departments:
            statistic.append({"name": department.name, "total":Production.statistic(department_id= department.id)["total"],"best":Teacher.best(department_id=department.id)})
        return statistic
            