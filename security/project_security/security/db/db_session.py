from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from security.db.url import __DB_CONFIG

engine = create_engine(__DB_CONFIG)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()