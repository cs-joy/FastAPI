from app.config import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(
    settings.db_url,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=True if settings.environment == "development" else False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = declarative_base()
    try:
        yield db
    finally:
        db.close()

