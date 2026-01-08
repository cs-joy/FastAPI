from app.config import settings

from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography.hazmat.backends import default_backend
from typing import Dict, Any
from datetime import timedelta, datetime, timezone
import uuid
from jose import JWTError, jwt

def load_private_key():
    with open(settings.JWT_PRIVATE_KEY_PATH, "rb") as key_file:
        private_key = load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key

def load_public_key():
    with open(settings.JWT_PUBLIC_KEY_PATH, "rb") as key_file:
        public_key = load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return public_key

def create_access_token(data: Dict[str, Any], expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(),
        "type": "access",
        "jti": str(uuid.uuid4())
    })

    private_key = load_private_key()
    encoded_jwt = jwt.encode(
        to_encode,
        private_key, # experiment >>
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt

def create_refresh_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    data = {
        "sub": user_id,
        "exp": expire,
        "ita": datetime.now(timezone.utc),
        "type": "refresh",
        "jti": str(uuid.uuid4())
    }

    privaye_key = load_private_key()
    return jwt.encode(data, privaye_key, algorithm=settings.JWT_ALGORITHM)

def verify_token(token: str) -> Dict[str, Any]:
    try:
        public_key = load_public_key()
        payload = jwt.decode(
            token,
            public_key,algorithms=settings.JWT_ALGORITHM
        )
        return payload
    except JWTError:
        return None

def generate_csrf_token() -> str:
    return str(uuid.uuid4())

def hash_token(token: str) -> str:
    import hashlib
    return hashlib.sha256(token.encode()).hexdigest()

