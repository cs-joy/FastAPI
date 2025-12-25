# Simple OAuth2 with Password and Bearer
# source: https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/

# # Get the `username` and `password`
#: source: https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/#get-the-username-and-password
 
# # # `scope`
#: source: https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/#scope
'''
The spec also says that the client can send another form field "scope"
The form field name is `scope` (in singular), but it is actually a long string with "scopes" separated by spaces
Each "scope" is just a string (without spaces).
They are normally used to declare specific security permissions, for example:
- `users:read` or `users:write` are common examples
- `instagram_basic` is used by Facebook / Instagram
- `https://www.googleapis.com/auth/drive` is used by Google.

'Info'
In OAuth2 a "scope" is just a string that declares a specific permission required.
It doesn't matter if it has other character like `:` or if it is a URL.
Those details are implementation specific.
For OAuth2 they are just strings.
'''

# Code to get the `username` and `password`
# # `OAuth2PasswordRequestForm`
# First, import `OAuth2PasswordRequestForm` , and use it as a dependency with `Depends` in the path operation for `/token`:
from typing import Annotated
import logfire
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

fake_users_db = {
    "john_doe": {
        "username": "john_doe",
        "full_name": "John Doe",
        "email": "john@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret123",
        "disabled": True,
    }
}

app = FastAPI()
logfire.configure()
logfire.instrument_fastapi(app)

def fake_hash_password(password: str):
    return "fakehashed" + password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def fake_decode_token(token):
    # this doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user  = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

@app.post('/token')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    
    return {
        "access_token": user.username,
        "token_type": "bearer"
    }

@app.get('/users/me')
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


# # Check the password
#: source: https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/#check-the-password

# # # About `**user_dict`
# source: https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/#about-user-dict

# # Return the token
