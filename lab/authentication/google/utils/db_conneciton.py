import os
from functools import lru_cache
from fastapi import FastAPI
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

from utils.config import Settings

load_dotenv()

@lru_cache
def get_settings():
    return Settings()

engine = create_engine(os.environ['DB_URL'])
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()