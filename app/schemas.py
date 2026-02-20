from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import List, Optional


class DepartmentBase(BaseModel):
    name: str
    location: str


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentResponse(DepartmentBase):
    id: int

    class Config:
        orm_mode = True


class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    salary: float = Field(..., ge=10000)
    start_date: date
    department_id: int


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeResponse(EmployeeBase):
    id: int

    class Config:
        orm_mode = True

#Nested response yapıları
class DepartmentNested(BaseModel):
    id: int
    name: str
    location: str

    class Config:
        orm_mode = True

class EmployeeNested(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    salary: float
    start_date: date

    class Config:
        orm_mode = True

class EmployeeWithDepartmentInfo(EmployeeNested):
    department: DepartmentNested

class DepartmentWithEmployeeInfo(DepartmentNested):
    employees: list[EmployeeNested]