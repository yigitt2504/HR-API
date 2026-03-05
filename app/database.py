from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
from .config import settings
import time

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def wait_for_db(retries=10, delay=3):
    for i in range(retries):
        try:
            conn = engine.connect()
            conn.close()
            print("Postgres hazır!")
            return
        except OperationalError:
            print(f"Postgres bekleniyor... ({i+1}/{retries})")
            time.sleep(delay)
    raise Exception("Postgres bağlanılamadı!")
