from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.orm import Session

from utils.db_conneciton import db_session
from utils.schema import User

router = APIRouter()

@router.get("/users/me")
async def view_profile(User, db: Annotated[Session, Depends(db_session)]):
    #
    return {
        "user": "user"
    }


@router.get("/users/test")
async def view_profile_test():
    return {
        "message": "grettings!"
    }

@router.get("/users/auth")
async def read_own_items():
    auth_method = "blabla1"
    return {
        "message": f"Authenticated via {auth_method}",
        "user": "user",
    }