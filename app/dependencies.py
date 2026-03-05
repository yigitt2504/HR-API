from fastapi import Header, HTTPException, Depends
from .database import SessionLocal
from sqlalchemy.orm import Session

API_KEY = "***REMOVED***"

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()