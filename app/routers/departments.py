from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import models, schemas
from app.dependencies import get_db, verify_api_key
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.post("", response_model=schemas.DepartmentResponse, status_code=201, dependencies=[Depends(verify_api_key)])
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    db_department = models.Department(**department.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    logger.info("Departman kaydedildi.")
    return db_department


@router.get("", response_model=list[schemas.DepartmentResponse], dependencies=[Depends(verify_api_key)])
def list_departments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Department).offset(skip).limit(limit).all()


@router.get("/{department_id}", response_model=schemas.DepartmentWithEmployeeInfo, dependencies=[Depends(verify_api_key)])
def get_department(department_id: int, db: Session = Depends(get_db)):
    department = db.query(models.Department).filter(models.Department.id == department_id).first()

    if not department:
        raise HTTPException(status_code=404, detail="Departman bulunamadı.")

    return department


@router.put("/{department_id}", response_model=schemas.DepartmentResponse, dependencies=[Depends(verify_api_key)])
def update_department(department_id: int, department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    db_department = db.query(models.Department).filter(models.Department.id == department_id).first()

    if not db_department:
        raise HTTPException(status_code=404, detail="Departman bulunamadı.")

    for key, value in department.dict().items():
        setattr(db_department, key, value)

    db.commit()
    db.refresh(db_department)
    return db_department


@router.delete("/{department_id}", status_code=204, dependencies=[Depends(verify_api_key)])
def delete_department(department_id: int, db: Session = Depends(get_db)):
    db_department = db.query(models.Department).filter(models.Department.id == department_id).first()

    if not db_department:
        raise HTTPException(status_code=404, detail="Departman bulunamadı.")

    db.delete(db_department)
    db.commit()