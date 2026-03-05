from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
import logging
from app.database import engine, Base, wait_for_db
from app import models
from app.routers import departments, employees

wait_for_db()

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.exception_handler(IntegrityError)
async def integrity_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": "Veri bütünlüğü hatası."},
    )

@app.get("/")
def read_root():
    return {"message": "HR API is running"}

app.include_router(departments.router)
app.include_router(employees.router)