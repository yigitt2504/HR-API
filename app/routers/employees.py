from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import models, schemas
from app.dependencies import get_db, verify_api_key
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post("", response_model=schemas.EmployeeResponse, status_code=201, dependencies=[Depends(verify_api_key)])
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):

    department = db.query(models.Department).filter(models.Department.id == employee.department_id).first()
    if not department:
        raise HTTPException(status_code=400, detail="Department bulunamadı.")

    db_employee = models.Employee(**employee.dict())
    db.add(db_employee)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Bu email zaten kayıtlı.")

    db.refresh(db_employee)
    return db_employee


@router.get("", response_model=list[schemas.EmployeeResponse], dependencies=[Depends(verify_api_key)])
def list_employees(
    min_salary: float | None = None,
    max_salary: float | None = None,
    department_id: int | None = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(models.Employee)

    if min_salary is not None:
        query = query.filter(models.Employee.salary >= min_salary)

    if max_salary is not None:
        query = query.filter(models.Employee.salary <= max_salary)

    if department_id is not None:
        query = query.filter(models.Employee.department_id == department_id)

    return query.offset(skip).limit(limit).all()


@router.get("/{employee_id}", response_model=schemas.EmployeeWithDepartmentInfo, dependencies=[Depends(verify_api_key)])
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Çalışan bulunamadı.")

    return employee


@router.put("/{employee_id}", response_model=schemas.EmployeeResponse, dependencies=[Depends(verify_api_key)])
def update_employee(employee_id: int, employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()

    if not db_employee:
        raise HTTPException(status_code=404, detail="Çalışan bulunamadı.")

    for key, value in employee.dict().items():
        setattr(db_employee, key, value)

    db.commit()
    db.refresh(db_employee)
    return db_employee


@router.delete("/{employee_id}", status_code=204, dependencies=[Depends(verify_api_key)])
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Çalışan bulunamadı.")

    db.delete(employee)
    db.commit()