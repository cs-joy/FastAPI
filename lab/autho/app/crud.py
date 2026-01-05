from sqlalchemy.orm import Session
import uuid

from app.models import User, OAuthAccount, RefreshToken
from app.schemas import UserCreate, UserUpdate, OAuthAccountCreate
from datetime import datetime, timezone

def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: uuid.UUID) -> User:
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: uuid.UUID, user_update: UserUpdate) -> User:
    db_user = get_user_by_id(db, user_id)
    if db_user:
        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def get_oauth_account(db: Session, provider: str, provider_user_id: str) -> OAuthAccount | None:
    return db.query(OAuthAccount).filter(
        OAuthAccount.provider == provider,
        OAuthAccount.provider_user_id == provider_user_id
    ).first()

def create_oauth_account(db: Session, oauth_account: OAuthAccountCreate, user_id: uuid.UUID) -> OAuthAccount:
    db_oauth = OAuthAccount(
        user_id = user_id,
        **oauth_account.model_dump()
    )
    db.add(db_oauth)
    db.commit()
    db.refresh(db_oauth)
    return db_oauth

def update_oauth_account(db: Session, oauth_id: uuid.UUID, update_data: dict) -> OAuthAccount:
    db_oauth = db.query(OAuthAccount).filter(OAuthAccount.id == oauth_id).first()
    if db_oauth:
        for field, value in update_data.items():
            setattr(db_oauth, field, value)
        db.commit()
        db.refresh(db_oauth)
    return db_oauth

def create_refresh_token_record(db: Session, 
                                user_id: uuid.UUID, 
                                token: str, 
                                expires_at, 
                                user_agent: str = None, 
                                ip_addres: str = None) -> RefreshToken:
    from app.utils.security import hash_token
    db_token = RefreshToken(
        user_id = user_id,
        token=hash_token
    )
    return db_token

def get_refresh_token(db: Session, token: str) -> RefreshToken:
    from app.utils.security import hash_token
    hashed_token = hash_token(token)
    return db.query(RefreshToken).filter(
        RefreshToken.token == hashed_token,
        RefreshToken.revoked == False,
        RefreshToken.expires_at > datetime.now(timezone.utc)
    ).first()

def revoke_refresh_token(db: Session, token: str) -> None:
    from app.utils.security import hash_token
    hashed_token = hash_token(token)
    db.query(RefreshToken).filter(RefreshToken.token == hashed_token).update(
        {"revoked": True}
    )
    db.commit

def revoke_all_refresh_tokens(db: Session, user_id: uuid.UUID) -> None:
    db.query(RefreshToken).filter(RefreshToken.user_id == user_id).update(
        {"revoked": True}
    )
    db.commit()