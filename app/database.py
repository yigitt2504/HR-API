from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
import os
import time

engine = create_engine(settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

while True:
    try:
        with engine.connect() as conn:
            print("Postgres hazır!")
            break
    except Exception as e:
        print("Postgres bekleniyor...", e)
        time.sleep(2)

