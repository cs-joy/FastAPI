# OAuth2 with Password (and hashing), Bearer with JWT tokens
#: source: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

'''
Now that we have all the security flow, let's make the application actually secure, using JWT tokens and secure password hashing.

# # About JWT
JWT -> JSON Web Tokens
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c

it's not encrypted, so, anyone could recover the information from the contents.
But it's signed. So, when you receive a token that you emitted, you can verify that you actually emitted it.

That way, you can create a token with an expiration of let's say, 1 week. And then when the user comes back the next day with the token, you know that user is still logged in to your system.

After a week, the token will be expired and the user will not be authorized and will have to sign in again to get a new token. And if the user (or a third party) tried to modify the token to change the expiration, you would be able to discover it, because the signatures would not match.

If you want to play with JWT tokens and see how they work, check : https://www.jwt.io/
'''

# # Install PyJWT

# # Password Hashing
'''
"Hashing" means converting some content (a password in this case) into a sequence of bytes (just a string) that looks like gibberish.
Whenever you pass exactly the same content (exactly the same password) you get excatly the same gibberish.

But you cannot convert from the gibberish back to the password.
'''

# # # Why use password hashing: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#why-use-password-hashing

# # Install pwdlib
'''
With pwdlib, you could even configure it to be able to read passwords created by Django, a Flask security plug-in or many others.

So, you would be able to, for example, share the same data from a Django application in a database with a FastAPI application. Or gradually migrate a Django application using the same database.

And your users would be able to login from your Django app or from your FastAPI app, at the same time.
'''

# # Hash and verify the passwords
#: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#hash-and-verify-the-passwords
'''
Create a utility function to hash a password coming from the user.
And another utility to verify if a received a password matches the hash stored.
And another one to authenticate and return a user.
'''

from pydantic import BaseModel
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends, HTTPException, status
import jwt
from typing import Annotated
from jwt.exceptions import InvalidTokenError

from datetime import timedelta, datetime, timezone

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "john@doe.io",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc",
        "disabled": False,
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str

class  TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def verify_password(plain_text_password: str, hashed_password: str):
    return password_hash.verify(plain_text_password, hashed_password)

def get_password_hash(password: str):
    return password_hash.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None  = None):
    to_encode = data.copy()
    print(f"expires_delta: {expires_delta}")
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
        print(f"expire = datetime.now(timezone.utc) + expires_delta: {expire}")
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        print(f"expire_e = datetime.now(timezone.utc) + timedelta(minutes=15): {expire}")
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
                                to_encode, 
                                SECRET_KEY, 
                                algorithm=ALGORITHM
                            )
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Coulde not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"payload: {payload}")
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

# # # # # # #
@app.post('/token/')
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data = {
            "sub": user.username
        },
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.get('/users/me/', response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user

@app.get('/users/me/items/')
async def read_own_items(current_user: Annotated[User, Depends(get_current_active_user)]):
    return [
        {
            "item_id": "Foo",
            "owner": current_user.username
        }
    ]