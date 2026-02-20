from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
import os
import time

DATABASE_URL = settings.DATABASE_URL


max_retries = 10
while True:
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            pass
        break
    except OperationalError:
        max_retries -= 1
        if max_retries == 0:
            raise
        print("Postgres bekleniyor...")
        time.sleep(2)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


