from fastapi import FastAPI, HTTPException, Header
from sqlalchemy import text
from .database import engine
from . import models, schemas
from .database import SessionLocal
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = "api_key123"

def verify_api_key(x_api_key: str = Header(...)):
      if x_api_key != API_KEY:
            raise HTTPException(status_code=401, detail="Unauthorized")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.exception_handler(IntegrityError)
async def integrity_exception_handler(request, exc):
    return JSONResponse(
        logger.error("Veri bütünlüğü hatası."),
        status_code=400,
        content={"detail": "Veri bütünlüğü hatası."},
    )

@app.get("/")
def read_root():
    logger.info("HR API çalışıyor.")
    return {"message": "HR API is running"}

@app.post("/departments", response_model=schemas.DepartmentResponse, status_code=201, dependencies=[Depends(verify_api_key)])
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    logger.info("Departman kaydedildi.")
    db_department = models.Department(**department.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

@app.get("/departments", response_model=list[schemas.DepartmentResponse], dependencies=[Depends(verify_api_key)])
def list_departments(db: Session = Depends(get_db)):
    logger.info("Departmanlar listelendi.")
    return db.query(models.Department).all()

@app.put("/departments/{department_id}", response_model=schemas.DepartmentResponse, dependencies=[Depends(verify_api_key)])
def update_department(department_id: int, department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    logger.info("Departman bilgisi güncellendi.")
    db_department = db.query(models.Department).filter(models.Department.id == department_id).first()

    if not db_department:
        logger.error("Departman bulunamadı.")
        raise HTTPException(status_code=404, detail="Departman bulunamadı.")

    for key, value in department.dict().items():
        setattr(db_department, key, value)

    db.commit()
    db.refresh(db_department)
    return db_department

@app.delete("/departments/{department_id}", status_code=204, dependencies=[Depends(verify_api_key)])
def delete_department(department_id: int, db: Session = Depends(get_db)):
    logger.info("Departman silindi.")
    db_department = db.query(models.Department).filter(models.Department.id == department_id).first()

    if not db_department:
        raise HTTPException(status_code=404, detail="Departman bulunamadı.")

    db.delete(db_department)
    db.commit()
    return

@app.post("/employees", response_model=schemas.EmployeeResponse, status_code=201, dependencies=[Depends(verify_api_key)])
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
	
	department = db.query(models.Department).filter(models.Department.id == employee.department_id).first()
	if not department:
		raise HTTPException(status_code=400, detail="Department bulunamadı.")

	db_employee = models.Employee(**employee.dict())
	db.add(db_employee)
	try:
		logger.info("Çalışan kaydedildi.")
		db.commit()
	except IntegrityError:
		db.rollback()
		logger.error("Bu email zaten kayıtlı.")
		raise HTTPException(status_code=400, detail="Bu email zaten kayıtlı.")
      
	db.refresh(db_employee)
	return db_employee

@app.get("/employees", response_model=list[schemas.EmployeeResponse], dependencies=[Depends(verify_api_key)])
def list_employees(
	min_salary: float | None = None,
	max_salary: float | None = None,
    department_id: int | None = None,
    skip: int=0,
    limit: int=10,
    db: Session = Depends(get_db)
):
     
	query = db.query(models.Employee)
      
	if min_salary is not None:
		query = query.filter(models.Employee.salary >= min_salary)

	if max_salary is not None:
		query = query.filter(models.Employee.salary <= max_salary)

	if department_id is not None:
		query = query.filter(models.Employee.department_id == department_id)

	return query.all()
		

@app.get("/employees/{employee_id}", response_model=schemas.EmployeeWithDepartmentInfo, dependencies=[Depends(verify_api_key)])
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()

    if not employee:
        logger.error("Çalışan bulunamadı.")
        raise HTTPException(status_code=404, detail="Çalışan bulunamadı.")

    return employee

@app.get("/departments/{department_id}", response_model=schemas.DepartmentWithEmployeeInfo, dependencies=[Depends(verify_api_key)])
def get_department(department_id: int, db: Session = Depends(get_db)):
    
	department = db.query(models.Department).filter(models.Department.id == department_id).first()
     
	if not department:
		logger.error("Departman bulunamadı.")
		raise HTTPException(status_code=404, detail="Departman bulunamadı.")

	return department

@app.put("/employees/{employee_id}", response_model=schemas.EmployeeResponse, dependencies=[Depends(verify_api_key)])
def update_employee(employee_id: int, employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):

    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()

    if not db_employee:
        logger.error("Çalışan bulunamadı.")
        raise HTTPException(status_code=404, detail="Çalışan bulunamadı.")

    for key, value in employee.dict().items():
        setattr(db_employee, key, value)

    db.commit()
    db.refresh(db_employee)
    return db_employee

@app.delete("/employees/{employee_id}", status_code=204, dependencies=[Depends(verify_api_key)])
def delete_employee(employee_id: int, db: Session = Depends(get_db)):

	logger.info("Çalışan silindi")
	employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()

	if not employee:
		raise HTTPException(status_code=404, detail="Çalışan bulunamadı.")

	db.delete(employee)
	db.commit()
	return