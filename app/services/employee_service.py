from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.repositories.employee_repository import (
    employee_repository,
    list_employees as repo_list_employees,
    get_employee_by_id
)
from app import schemas, models
from app.config import MIN_SALARY


def list_employees(
    db: Session,
    skip: int,
    limit: int,
    min_salary: float | None = None,
    max_salary: float | None = None,
    department_id: int | None = None
):
    if min_salary is None:
        min_salary = MIN_SALARY

    return repo_list_employees(db, skip, limit, min_salary, max_salary, department_id)

def get_employee(db: Session, employee_id: int):
    employee = get_employee_by_id(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Çalışan bulunamadı.")
    return employee

def create_employee(db: Session, employee: schemas.EmployeeCreateUI):
    department = db.query(models.Department).filter(
        models.Department.name == employee.department_name
    ).first()
    if not department:
        raise HTTPException(status_code=400, detail="Department bulunamadı.")

    employee_data = schemas.EmployeeCreate(
        first_name=employee.first_name,
        last_name=employee.last_name,
        email=employee.email,
        salary=employee.salary,
        start_date=employee.start_date,
        department_id=department.id
    )

    try:
        return employee_repository.create_employee(db, employee_data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Bu email zaten kayıtlı.")

def update(db: Session, employee_id: int, employee: schemas.EmployeeCreateUI):
    db_employee = get_employee(db, employee_id)

    department = db.query(models.Department).filter(
        models.Department.name == employee.department_name
    ).first()
    if not department:
        raise HTTPException(status_code=400, detail="Department bulunamadı.")

    employee_data = schemas.EmployeeCreate(
        first_name=employee.first_name,
        last_name=employee.last_name,
        email=employee.email,
        salary=employee.salary,
        start_date=employee.start_date,
        department_id=department.id
    )

    return employee_repository.update(db, db_employee, employee_data)


def delete_employee(db: Session, employee_id: int):
    db_employee = get_employee(db, employee_id)
    employee_repository.delete_employee(db, db_employee)