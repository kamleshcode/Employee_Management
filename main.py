from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from pydantic import BaseModel, EmailStr, Field
from typing import Optional,Annotated
from sqlalchemy.orm import Session

from database import Base, engine, get_db

app = FastAPI()

#SQLAlchemy Model
class Employee(Base):
    __tablename__ = "Employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    department = Column(String(100))
    salary = Column(Float)
    phoneNumber = Column(String(20))
    isActive = Column(Boolean, default=True)

Base.metadata.create_all(bind=engine)

#Pydantic Class
class EmployeeSchema(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., description="Employee Name", max_length=20)
    email: EmailStr
    department: Annotated[str, Field(..., description="Department Name", max_length=20)]
    salary: Annotated[float, Field(description="Salary of Employee", gt=0, examples=['2000.00'])]
    phoneNumber: Annotated[str, Field(max_length=20, description="Phone Number", examples=['+1 555 555'])]
    isActive: bool = Field(..., description="Is Employee Active")

class EmployeeToggleSchema(BaseModel):
    isActive: bool


@app.get("/employees")
def get_all(db : Session = Depends(get_db)):
    employees = db.query(Employee).all()
    return employees

@app.get("/employees/{id}")
def get_one(emp_id : int, db : Session = Depends(get_db)):
    employee = db.query(Employee).filter(id = emp_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@app.post("/employees")
def create_employees(emp: EmployeeSchema,db : Session = Depends(get_db)):
    employee = db.query(Employee).filter(id= emp.id).first()
    if employee is not None:
        raise HTTPException(status_code=400, detail="Email already exists")
    new_employee = Employee(**emp.model_dump(exclude={"id"}))
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

@app.delete("/employees/{id}")
def delete_employees(emp_id : int, db : Session = Depends(get_db)):
    employee = db.query(Employee).filter(id = emp_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(employee)
    db.commit()
    return employee

@app.put("/employees/{id}")
def update_employee(emp_id : int, emp: EmployeeSchema,db : Session = Depends(get_db)):
    employee = db.query(Employee).filter_by(id=emp_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    updates_data = emp.model_dump(exclude_unset=True,exclude={"id"})
    for key, value in updates_data.items():
        setattr(employee, key, value)
        db.commit()
        db.refresh(employee)
        return employee
    return employee

@app.patch("/employees/{id}/status")
def toggle_status(emp_id : int,status_data : EmployeeToggleSchema, db : Session = Depends(get_db)):
    employee = db.query(Employee).filter_by(id=emp_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    employee.isActive = status_data.isActive
    db.commit()
    db.refresh(employee)
    return employee




