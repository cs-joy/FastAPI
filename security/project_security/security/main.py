from typing import Annotated
from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session

from security.db.db_session import engine, db_session
from security.db.model import Base
from security.utils.schema import User, UserInDB
from security.utils.utils_resources import add_new_user


app = FastAPI(title="Security - RSA256", description="Security Framework with jwt()", version="0.0.1")

Base.metadata.create_all(bind=engine)

@app.get('/health')
async def get_status():
    return {
        "status": "active"
    }

@app.post('/add-user/', status_code=status.HTTP_201_CREATED)
async def register_user(user: UserInDB, db: Annotated[Session, Depends(db_session)]) -> User:
    return await add_new_user(user, db)