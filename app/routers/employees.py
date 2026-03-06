from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas
from app.dependencies import get_db, verify_api_key
from app.services import employee_service
from app.repositories import employee_repository

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.post("", response_model=schemas.EmployeeResponse, status_code=201, dependencies=[Depends(verify_api_key)])
def create_employee(employee: schemas.EmployeeCreateUI, db: Session = Depends(get_db)):
    return employee_service.create_employee(db, employee)

@router.get(
    "",
    response_model=list[schemas.EmployeeResponse],
    dependencies=[Depends(verify_api_key)]
)
def list_employees(
    min_salary: float | None = None,
    max_salary: float | None = None,
    department_id: int | None = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    return employee_service.list_employees(
        db,
        skip,
        limit,
        min_salary,
        max_salary,
        department_id
    )


@router.get("/{employee_id}", response_model=schemas.EmployeeWithDepartmentInfo)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    return employee_service.get_employee(db, employee_id)

@router.put("/{employee_id}", response_model=schemas.EmployeeResponse, dependencies=[Depends(verify_api_key)])
def update(employee_id: int, employee: schemas.EmployeeCreateUI, db: Session = Depends(get_db)):
    return employee_service.update(db, employee_id, employee)

@router.delete(
    "/{employee_id}",
    status_code=204,
    dependencies=[Depends(verify_api_key)]
)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee_service.delete_employee(db, employee_id)
