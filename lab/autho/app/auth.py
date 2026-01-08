import time
import httpx
import secrets
import jwt as pyjwt
from authlib.jose import jwt as auth_jwt
from authlib.integrations.starlette_client import OAuth

from app.config import settings
from typing import Dict, Any

# oauth config
oauth = OAuth()

# debug
print('google_client_id: {google_client_id}')

# google auth
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile',
        'prompt': 'select_account'
    }
)

async def get_google_user_info(access_token: str) -> Dict[str, Any] | None:
    # fetch user info from google using access token
    async with httpx.AsyncClient() as client:
        try:
            # verify token
            token_info_response = await client.get(
                f"https://oauth2.googleapis.com/tokeninfo",
                params={
                    "access_token": access_token
                }
            )
            token_info_response.raise_for_status()

            # get user info
            userinfo_response = await client.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            userinfo_response.raise_for_status()
            return userinfo_response.json()
        except httpx.HTTPError:
            return None

async def exchange_google_code(code: str, redirect_uri: str) -> Dict[str, Any] | None:
    # exchange authorization code for tokens
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://oauth2.googleapis.com/token",
                data = {
                    "code": code,
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "redirect_uri": redirect_uri or settings.GOOGLE_REDIRECT_URI,
                    "grant_type": "authorization_code"
                }
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError:
            return None
    
async def verify_apple_token(id_token: str) -> Dict[str, Any] | None:
    # verify apple id token
    try:
        # get apple's public keys
        async with httpx.AsyncClient() as client:
            keys_response = await client.get("https://appleid.apple.com/auth/keys")
            keys_response.raise_for_status()
            jwk_set = keys_response.json()
        # decode and verify token
        claims = auth_jwt.decode(
            id_token,
            jwk_set,
            claims_options= {
                "iss": {
                    "essential": True,
                    "value": "https://appleid.apple.com",
                },
                "aud": {
                    "essential": True,
                    "value": settings.APPLE_CLIENT_ID
                },
                "exp": {
                    "essential": True
                }
            }
        )
        claims.validate()
        return claims
    except Exception:
        return None

async def exchange_apple_code(code: str, redirect_uri: str) -> Dict[str, Any] | None:
    # exchange apple authentication code for tokens
    import time

    # create client secret
    client_secret = generate_apple_client_secret()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://appleid.apple.com/auth/token",
                data = {
                    "code": code,
                    "client_id": settings.APPLE_CLIENT_ID,
                    "client_secret": client_secret,
                    "redirect_uri": redirect_uri or settings.APPLE_REDIRECT_URI,
                    "grant_type": "authorization_code"
                }
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"Apple token exchange error: {e}")
            return None
        
def generate_apple_client_secret() -> str:
    # generate client secret through the private key
    from cryptography.hazmat.primitives import serialization

    with open(settings.APPLE_PRIVATE_KEY_PATH, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password = None,
        )

    now = int(time.time())
    payload = {
        "iss": settings.APPLE_TEAM_ID,
        "iat": now,
        "exp": now + 15777000,   # 6 months
        "aud": "https://appleid.apple.com",
        "sub": settings.APPLE_CLIENT_ID
    }

    headers = {
        "alg": "ES256",
        "kid": settings.APPLE_KEY_ID
    }

    return pyjwt.encode(payload, private_key, algorithm="ES256", headers=headers)

def generate_state_token() -> str:
    # generate secure state token for OAuth flow
    return secrets.token_urlsafe(32)

def validate_state_token(state: str, expected_state: str) -> bool:
    # validate state token to prevent CSRF
    return secrets.compare_digest(state, expected_state)