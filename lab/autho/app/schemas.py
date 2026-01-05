from enum import Enum
from pydantic import BaseModel, EmailStr, field_validator
import uuid
from datetime import datetime
from typing import Dict, Any


class TokenType(str, Enum):
    BEARER = "bearer"
    REFRESH = "refresh"

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = TokenType.BEARER
    expires_in: int

class TokenData(BaseModel):
    userd_id: str
    email: str | None = None

class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None
    picture: str | None = None

class UserCreate(UserBase):
    email_verified: bool = False

class UserUpdate(BaseModel):
    full_name: str | None = None
    picture: str | None = None

class UserInDB(UserBase):
    id: uuid.UUID
    email_verified: bool
    is_active: bool
    is_disabled: bool
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True
    
class OAuthAccountBase(BaseModel):
    proivder: str
    provider_user_id: str

class OAuthAccountCreate(OAuthAccountBase):
    access_token: str
    refresh_token: str | None = None
    expires_at: datetime | None = None

class GoogleAuthRequest(BaseModel):
    code: str
    redirect_uri: str | None = None
    state: str | None = None

class AppleAuthRequest(BaseModel):
    code: str
    id_token: str | None = None
    user: Dict[str, Any] | None = None
    redirect_uri: str | None = None
    state: str | None = None

    @field_validator('user')
    def validate_user(cls, v):
        if v and 'name' in v:
            # ensures name structure is correct
            name = v.get('name', {})
            if isinstance(name, dict):
                v['name'] = {
                    'firstName': name.get('firstName', ''),
                    'lastName': name.get('lastName', '')
                }
        return v
    

