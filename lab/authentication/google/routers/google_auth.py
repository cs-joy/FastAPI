from fastapi import APIRouter, Request, Depends
from functools import lru_cache
from authlib.integrations.starlette_client import OAuth
import os
from typing import Annotated

from utils.config import Settings
from .auth import create_access_token

router = APIRouter()

@lru_cache
def get_settings():
    return Settings()

oauth = OAuth()
oauth.register(
    name="google",
    client_id=os.environ['GOOGLE_CLIENT_ID'],
    client_secret=os.environ['GOOGLE_CLIENT_SECRET'],
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params={"scope": "openid email profile"},
    access_token_url="https://oauth2.googleapis.com/token",
    client_kwargs={"scope": "openid email profile"},
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration"
)

@router.get("/auth/google")
async def auth_google(request: Request):
    return await oauth.google.authorize_redirect(request, redirect_uri="http://localhost:8000/auth/google/callback")

@router.get("/auth/google/callback")
async def google_callback(request: Request, db: Annotated[Session, Depends(db_session)]):
    try:
        token = await oauth.google_authorize_access_token(request)
        user_info = token.get("userinfo") or {}

        username = user_info.get("email")
        
        access_token = create_access_token(
            db,
            data = {"sub": username}
            expires_delta=timedelta(minutes=db.ACCESS_TOKEN_EXPIRE_MINUTES),
            auth_method="google"
        )

        return {
            "access_token": access_token,
            "token": token
        }
    except Exception as e:
        import traceback
        print("Error: ", traceback.format_exc())
        return {
            "error": str(e)
        }
