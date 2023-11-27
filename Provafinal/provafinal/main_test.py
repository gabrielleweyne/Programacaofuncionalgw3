from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import DateTime, Float, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey

import uvicorn

import os

user = "root"
password = "root"
mysql = "localhost:3306"
database = "provafinal"

app = FastAPI()


engine = create_engine(f"mysql+pymysql://{user}:{password}@{mysql}/{database}?charset=utf8mb4")


Sessionlocal = sessionmaker(autoflush=False, bind=engine)
session = Sessionlocal()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()


Base = declarative_base()

    
class Department(Base):
	__tablename__ = "department" 
	
	DepartmentID = Column(Integer, primary_key=True, index=True)
	Name = Column(String(50))
	Region = Column(String(50))
	
	Employees = relationship("Employee", back_populates="Department") 
	

class Employee(Base):
	__tablename__ = "employee" 
	
	EmployeeID = Column(Integer, primary_key=True, index=True)
	DepartmentID = Column(ForeignKey("department.DepartmentID")) 
	Name = Column(String(50))
	Birthday = Column(DateTime)
	Region = Column(String(50))
	Salary = Column(Float(10, 2))
	Job = Column(String(50))
	
	Department = relationship("Department", back_populates="Employees")
	JobHistory = relationship("JobHistory", back_populates="Employee")


class JobHistory(Base):
	__tablename__ = "job_history"
	
	JobHistoryID = Column(Integer, primary_key=True, index=True)
	EmployeeID = Column(ForeignKey("employee.EmployeeID")) 
	Title = Column(String(50))
	StartDate = Column(DateTime)
	EndDate = Column(DateTime)
	Salary = Column(Float(10, 2))
	Job = Column(String(50))

	Employee = relationship("Employee", back_populates="JobHistory")
	

	

Base.metadata.create_all(bind=engine)


@app.get("/departments")
def read_departments():
	
	departments = session.query(Department).all()
	
	departments_list = []
	
	for department in departments:
		
		departments_dict = {"id": department.DepartmentID, "name": department.Name, "region": department.Region}
		
		departments_list.append(departments_dict)
	
	return JSONResponse(content=departments_list)


@app.get("/departments/{department_id}")
def read_departments_id(department_id: int):
	
	department = session.query(Department).filter(Department.DepartmentID == department_id).first()
	
	departments_dict = {"id": department.DepartmentID, "name": department.Name, "region": department.Region}
	
	return JSONResponse(content=departments_dict)


@app.post("/departments")
def create_department(name: str, region: str, ):
	
	department = Department(Name=name, Region=region)

	session.add(department)
	
	session.commit()
	
	return JSONResponse(content={"id": department.DepartmentID, "name": department.Name, "region": department.Region})


@app.put("/departments/{department_id}")
def update_department(department_id: int, name: str, region: str):
	
	department = session.query(Department).filter(Department.DepartmentID == department_id).first()
	
	department.Name = name
	
	department.Region = region
	
	session.commit()
	
	return JSONResponse(content={"id": department.DepartmentID, "name": department.Name, "region": department.Region})


@app.delete("/departments/{department_id}")
def delete_department(department_id: int):
	
	department = session.query(Department).filter(Department.DepartmentID == department_id).first()
	
	session.delete(department)
	
	session.commit()
	
	return JSONResponse(content={"id": department.DepartmentID, "name": department.Name, "region": department.Region})

#--------------------------------------------------------------------------------


@app.get("/employees")
def read_employees():
	
	employees = session.query(Employee).all()
	
	employees_list = []
	
	for employee in employees:
		
		employees_dict = {"id": employee.EmployeeID, "department_id": employee.DepartmentID, "name": employee.Name, "birthday": str(employee.Birthday), "region": employee.Region, "salary": float(employee.Salary), "job": employee.Job}
		
		employees_list.append(employees_dict)
	return JSONResponse(content=employees_list)


@app.get("/employees/{employee_id}")
def read_employee_id(employee_id: int):
	
	employee = session.query(Employee).filter(Employee.EmployeeID == employee_id).first()
	
	employees_dict = {"id": employee.EmployeeID, "department_id": employee.DepartmentID, "name": employee.Name, "birthday": str(employee.Birthday), "region": employee.Region, "salary": float(employee.Salary), "job": employee.Job}
	
	return JSONResponse(content=employees_dict)


@app.post("/employees")
def create_employee(department_id: int, name: str, birthday: str, region: str, salary: float, job: str):
	
	employee = Employee(DepartmentID=department_id, Name=name, Birthday=birthday, Region=region, Salary=salary, Job=job)
	
	session.add(employee)
	
	session.commit()
	
	return JSONResponse(content={"id": employee.EmployeeID, "department_id": employee.DepartmentID, "name": employee.Name, "birthday": str(employee.Birthday), "region": employee.Region, "salary": float(employee.Salary), "job": employee.Job})


@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, name: str, birthday: str, region: str, salary: float, job: str):
	
	employee = session.query(Employee).filter(Employee.EmployeeID == employee_id).first()
	
	employee.Name = name
	
	employee.Birthday = birthday
	
	employee.Region = region
	
	employee.Salary = salary
	
	employee.Job = job
	
	session.commit()
	
	return JSONResponse(content={"id": employee.EmployeeID, "department_id": employee.DepartmentID, "name": employee.Name, "birthday": str(employee.Birthday), "region": employee.Region, "salary": float(employee.Salary), "job": employee.Job})



@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
	
	employee = session.query(Employee).filter(Employee.EmployeeID == employee_id).first()	
	session.delete(employee)
	
	session.commit()
	
	return JSONResponse(content={"id": employee.EmployeeID, "department_id": employee.DepartmentID, "name": employee.Name, "birthday": str(employee.Birthday), "region": employee.Region, "salary": float(employee.Salary), "job": employee.Job})

#--------------------------------------------------------------------------------


@app.get("/jobhistory")
def read_jobhistory():

	jobhistory = session.query(JobHistory).all()
	
	jobhistory_list = []
	
	for jobhistory in jobhistory:
		
		jobhistory_dict = {"id": jobhistory.JobHistoryID, "employee_id": jobhistory.EmployeeID, "title": jobhistory.Title, "startdate": str(jobhistory.StartDate), "enddate": str(jobhistory.EndDate), "salary": float(jobhistory.Salary), "job": jobhistory.Job}
		
		jobhistory_list.append(jobhistory_dict)
	return JSONResponse(content=jobhistory_list)


@app.get("/jobhistory/{jobhistory_id}")
def read_jobhistory_id(jobhistory_id: int):
	
	jobhistory = session.query(JobHistory).filter(JobHistory.JobHistoryID == jobhistory_id).first()
	
	jobhistory_dict = {"id": jobhistory.JobHistoryID, "employee_id": jobhistory.EmployeeID, "title": jobhistory.Title, "startdate": str(jobhistory.StartDate), "enddate": str(jobhistory.EndDate), "salary": float(jobhistory.Salary), "job": jobhistory.Job}
	
	return JSONResponse(content=jobhistory_dict)


@app.post("/jobhistory")
def create_jobhistory(employee_id: int, title: str, startdate: str, enddate: str, salary: float, job: str):
	
	jobhistory = JobHistory(EmployeeID=employee_id, Title=title, StartDate=startdate, EndDate=enddate, Salary=salary, Job=job)
	
	session.add(jobhistory)
	
	session.commit()
	
	return JSONResponse(content={"id": jobhistory.JobHistoryID, "employee_id": jobhistory.EmployeeID, "title": jobhistory.Title, "startdate": str(jobhistory.StartDate), "enddate": str(jobhistory.EndDate), "salary": float(jobhistory.Salary), "job": jobhistory.Job})


@app.put("/jobhistory/{jobhistory_id}")
def update_jobhistory(jobhistory_id: int, title: str, startdate: str, enddate: str, salary: float, job: str):
	
	jobhistory = session.query(JobHistory).filter(JobHistory.JobHistoryID == jobhistory_id).first()
	
	jobhistory.Title = title
	
	jobhistory.StartDate = startdate
	
	jobhistory.EndDate = enddate
	
	jobhistory.Salary = salary
	
	jobhistory.Job = job
	
	session.commit()
	
	return JSONResponse(content={"id": jobhistory.JobHistoryID, "employee_id": jobhistory.EmployeeID, "title": jobhistory.Title, "startdate": str(jobhistory.StartDate), "enddate": str(jobhistory.EndDate), "salary": float(jobhistory.Salary), "job": jobhistory.Job})


@app.delete("/jobhistory/{jobhistory_id}")
def delete_jobhistory(jobhistory_id: int):

	jobhistory = session.query(JobHistory).filter(JobHistory.JobHistoryID == jobhistory_id).first()	# Remove o empregado do banco de dados
	session.delete(jobhistory)
	
	session.commit()
	
	return JSONResponse(content={"id": jobhistory.JobHistoryID, "employee_id": jobhistory.EmployeeID, "title": jobhistory.Title, "startdate": str(jobhistory.StartDate), "enddate": str(jobhistory.EndDate), "salary": float(jobhistory.Salary), "job": jobhistory.Job})


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)