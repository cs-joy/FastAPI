from app.database import get_db
from app.utils.security import verify_token
from app.crud import get_user_by_id, update_user
from app.schemas import UserInDB, UserUpdate

import uuid
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/user", tags=["users"])
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    # get current authenticated user
    payload = verify_token(credentials.credentials)
    if not payload or payload.get('type') != 'access':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    user_id = uuid.UUID(payload['sub'])
    user = get_user_by_id(db, user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    return user

@router.get('/me', response_model=UserInDB)
async def get_current_user_info(current_user: Annotated[UserInDB, Depends(get_current_user)]):
    # get current user information
    return current_user

@router.put('/me', response_model=UserInDB)
async def update_current_user_info(user_update: UserUpdate, current_user: Annotated[UserInDB, Depends(get_current_user)], db: Session = Depends(get_db)):
    # update current user information
    updated_user = update_user(db, current_user.id, user_update)
    return updated_user

@router.delete('/me')
async def delete_current_user(current_user: Annotated[UserInDB, Depends(get_current_user)], db: Session = Depends(get_db)):
    # delete current user account (soft delete)
    update_user(db, current_user.id, UserUpdate(is_active=False))
    return {
        "message": "Account deactivated successfully"
    }
