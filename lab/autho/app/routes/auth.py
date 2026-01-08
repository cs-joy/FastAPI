from app.auth import generate_state_token, exchange_google_code, get_google_user_info, exchange_apple_code, verify_apple_token
from app.config import settings
from app.schemas import GoogleAuthRequest, UserCreate, Token, AppleAuthRequest, OAuthAccountCreate
from app.database import get_db
from app.crud import get_user_by_email, create_user, get_oauth_account, update_oauth_account, create_oauth_account, create_refresh_token_record, get_refresh_token, get_user_by_id, revoke_refresh_token, revoke_all_refresh_tokens
from app.utils.security import create_access_token, create_refresh_token, verify_token

import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import secrets


router  = APIRouter(prefix='/auth', tags=["authentication"])
security = HTTPBearer()

@router.get("/google/login")
async def google_login(
    request: Request,
    redirect_uri: Optional[str] = None,
    state: Optional[str] = None
):
    # initiate google oauth login
    from authlib.integrations.starlette_client import OAuthError

    if not state:
        state = secrets.token_urlsafe(32)
        #state = generate_state_token()
        #request.session['oauth_state'] = state
    
    request.session['oauth_state'] = state
    
    redirect_uri = redirect_uri or settings.GOOGLE_REDIRECT_URI

    try:
        # genrate authorization URL
        google = request.app.state.oauth.google
        authorization_url = await google.authorize_redirect(
            request,
            redirect_uri,
            state=state
        )
        # redirect_uri = await request.app.state.oauth.google.authorize_redirect(
        #     request,
        #     redirect_uri,
        #     state = state
        # )
        return {
            "authorization_url": redirect_uri,
            "state": state
        }
    except OAuthError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"OAuth error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initiate Google Login: {str(e)}"
        )
    
@router.post("/google/callback")
async def google_callback(
    request: GoogleAuthRequest,
    db: Session = Depends(get_db),
    user_agent: str | None = None,
    ip_address: str | None = None
):
    # handle google oauth callback
    
    # exchange code for tokens
    token_data = await exchange_google_code(
        request.code,
        request.redirect_uri
    )

    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to exchange authorization code"
        )
    
    # get user info from Google
    user_info = await get_google_user_info(token_data['access_token'])

    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to fetch user info from Google"
        )
    
    # check if user exists by email
    user = get_user_by_email(db, user_info['email'])

    if not user:
        # create new user
        user_data = UserCreate(
            email = user_info['email'],
            full_name = user_info.get('name'),
            picture = user_info.get('picture'),
            email_verified=user_info.get('email_verified', False)
        )
        user = create_user(db, user_data)
    
    # check if OAuth account exists
    oauth_account = get_oauth_account(
        db,
        "google",
        user_info['sub']
    )

    # create or update OAuth account
    oauth_data = OAuthAccountCreate(
        proivder="google",
        provider_user_id=user_info['sub'],
        access_token=token_data['access_token'],
        refresh_token=token_data.get('refresh_token'),
        expires_at=datetime.now(timezone.utc) + timedelta(seconds=token_data.get('expires_in', 3600))
    )

    if oauth_account:
        update_oauth_account(db, oauth_account.id, oauth_data.model_dump())
    else:
        create_oauth_account(db, oauth_data, user.id)

    # create tokens
    access_token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email
        }
    )
    refresh_token = create_refresh_token(str(user.id))

    # store refresh token
    refresh_expires = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    create_refresh_token_record(
        db,
        user.id,
        refresh_token,
        refresh_expires,
        user_agent,
        ip_address
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

@router.post("/apple/callback")
async def apple_callback(
    request: AppleAuthRequest,
    db: Session = Depends(get_db),
    user_agent: str | None = None,
    ip_address: str | None = None
):
    # handle apple oauth callback
    token_data = await exchange_apple_code(
        request.code,
        request.redirect_uri
    )

    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to exchange authorization code with Apple",
        )

    # verify apple ID token
    id_token = token_data.get('id_token') or request.id_token
    if not id_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No ID token provided"
        )
    
    claims = await verify_apple_token(id_token)
    if not claims:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Apple ID token"
        )
    
    # extract user info
    email = claims.get('email')
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No email in Apple ID token"
        )

    # handle apple's unique email handling for private relay
    is_private_email = claims.get('is_private_email', False)
    apple_user_id = claims['sub']

    # get user info from apple's user parameter (if provided during first sign-in)
    user_name = None
    if request.user and 'name' in request.user:
        name_data = request.user['name']
        if name_data:
            user_name = f"{name_data.get('firstName', '')} {name_data.get('lastName', '')}".strip()
    
    # check if user exists by email
    user = get_user_by_email(db, email)

    if not user:
        # create new user
        user_data = UserCreate(
            email=email,
            full_name=user_name,
            email_verified=True, # apple emails are verified
        )
        user = create_user(db, user_data)
    
    # check if OAuth account exists
    oauth_account = get_oauth_account(db, 'apple', apple_user_id)

    # create or update OAuth account
    oauth_data = OAuthAccountCreate(
        proivder="apple",
        provider_user_id=apple_user_id,
        access_token=token_data['access_token'],
        refresh_token=token_data.get('refresh_token'),
        expires_at=datetime.now(timezone.utc) + timedelta(seconds=token_data.get('expires_in', 3600))
    )

    if oauth_account:
        update_oauth_account(db, oauth_account.id, oauth_data.model_dump())
    else:
        create_oauth_account(db, oauth_data, user.id)
    
    # create tokens
    access_token = create_access_token({
        "sub": str(user.id),
        "email": user.email
    })
    refresh_token = create_refresh_token(str(user.id))

    # store refresh token
    refresh_expires = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    create_refresh_token_record(
        db,
        user.id,
        refresh_token,
        user_agent,
        ip_address
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

@router.post("/refresh")
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db),
    user_agent: str | None = None,
    ip_address: str | None = None
):
    # refresh access token using refresh token
    
    # verify refresh token
    payload = verify_token(refresh_token)
    if not payload or payload.get('type') != 'refresh':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    # check if token exists in database and is not revoked
    token_record = get_refresh_token(db, refresh_token)
    if not token_record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found or revoked"
        )
    
    # get user
    user_id = uuid.UUID(payload['sub'])
    user = get_user_by_id(db, user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # revoke old refresh token
    revoke_refresh_token(db, refresh_token)

    # create new tokens
    access_token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email
        }
    )
    new_refresh_token = create_refresh_token(str(user.id))

    # store new refresh token
    refresh_expires = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    create_refresh_token_record(
        db,
        user.id,
        new_refresh_token,
        refresh_expires,
        user_agent,
        ip_address
    )

    return Token(
        access_token=access_token,
        refresh_token=new_refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

@router.post('/logout')
async def logout(refresh_token: str, db: Session = Depends(get_db)):
    # logout user by revoking refresh token
    revoke_refresh_token(db, refresh_token)
    return {
        "message": "Successfully logged out"
    }

@router.post("/logout/all/")
async def logout_all(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    # logout user from all devices
    
    # verify access token
    payload = verify_token(credentials.credentials)
    if not payload or payload.get('type') != 'access':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token"
        )
    # revoke all refresh tokens for user
    user_id = uuid.UUID(payload['sub'])
    revoke_all_refresh_tokens(db, user_id)

    return {
        "message": "Logged out from all devices"
    }