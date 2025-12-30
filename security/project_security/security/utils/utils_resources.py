from typing import Annotated
from fastapi import status, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from psycopg2 import OperationalError

from security.db.model import UserDB
from security.utils.schema import User, UserInDB


def hashing_password(password: str):
    return "fake"+password

async def add_new_user(user: UserInDB, db):

    if db.query(UserDB).filter(UserDB.username == user.username).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="username already exist")

    if db.query(UserDB).filter(UserDB.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="email already exist")

    new_user = UserDB(
                    username=user.username,
                    email=user.email,
                    password=hashing_password(user.password),
                    is_disabled=user.is_disabled
                )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return user
    except Exception as e:
        db.rollback()
        raise HTTPException(
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                detail="Failed to create user"
                            )
