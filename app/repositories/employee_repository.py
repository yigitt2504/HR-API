from sqlalchemy.orm import Session
from app.models import Employee
from app.repositories.base_repository import BaseRepository

employee_repository = BaseRepository(Employee)

def list_employees(
    db: Session,
    skip: int,
    limit: int,
    min_salary: float | None = None,
    max_salary: float | None = None,
    department_id: int | None = None
):
    query = db.query(Employee)
    if min_salary is not None:
        query = query.filter(Employee.salary >= min_salary)
    if max_salary is not None:
        query = query.filter(Employee.salary <= max_salary)
    if department_id is not None:
        query = query.filter(Employee.department_id == department_id)
    return query.offset(skip).limit(limit).all()

def get_employee_by_id(db: Session, employee_id: int):
    return db.query(Employee).filter(Employee.id == employee_id).first()