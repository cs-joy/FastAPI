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
#: source: https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/#return-the-token
#           `    return {"access_token": user.username, "token_type": "bearer"} `
'''
TIP: 
By the spec, we should return a JSON with `access_token` and `token_type`, the same as in the example,
This is something that you have to do yourself in your code, and make sure you use those JSON keys.
It's almost the only thing that you have to remember to do correctly yourself, to be compliant with the specifications.
For the rest, FastAPI handles it for you.
'''

# # Update the dependencies
# Now we are going to update our dependencies
# We want to get the `current_user` only if this user is active
# So, we create an additional dependency `get_current_active_user` that in turn uses `get_currenct_user` as a dependency.
# Both of these dependencies will just return an HTTP error if the user doesn't exists, or if is inactive.
# So, in our endpoint, we will only get a user if the user exists, was correctly authenticated, and is active.


# # # See it in action: 
# open the interactive docs: http://localhost:8000/docs

# # # # Authenticate:
# Click the "Authorize" button.
# Use the following credentials:
# User: john_doe
# Password: secret

# # Get your own user data

# # Inactive user
# try with an incactive user, authenticate with:
# user: alice
# password: secret123
# and try to use the operation `GET` with the path `/users/me/`
# you will get an "Inactive user" error


# # Recap::
# We can now have the tools to implement a complete security system based on `username` and `password` for our API.
# Using these tools, we can make the security system compatible with any database and with any user or data model.
# The only detail missing is that it is not actually "secure" yet.
#######################################################################
# let's go with the challenge
# challange::
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_URL = "postgresql://postgres:root@127.0.0.1:5431/secure_fastapi_bearer_challenge"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# SQLAlchemy User Model
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    email = Column(String)
    disabled = Column(Boolean,default=False)
    password = Column(String) # this should be hashed

# Create db table (run this once or use migrations in production)
Base.metadata.create_all(bind=engine)

# Pydantic user model
class UserPydantic(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserPydanticInDB(UserPydantic):
    password: str

# dependency - get db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# get user from db
def get_user_db(db, username: str):
    return db.query(UserDB).filter(UserDB.username == username).first()

# authenticate user by checking credentials against db
def authenticate_user(db, username: str, password: str):
    user = get_user_db(db, username)
    if not user:
        return False
    if user.password != password: # plain text check, replace with hashing mechanism
        return False
    return user

# Fake token creation
def create_access_token(data: dict):
    return data["sub"] # just `username` as token for this demo

# dependency to get current user from token
def get_curr_user(token: Annotated[str, Depends(oauth2_scheme)], db=Depends(get_db)):
    user = get_user_db(db, username=token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# dependency for active user
def get_curr_active_user(current_user: Annotated[UserPydantic, Depends(get_curr_user)]):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user

# login endpoint to get token
@app.post('/get-token/')
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db=Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# protected endpoint
@app.get('/users/profile/')
def read_users_me(current_user: Annotated[UserPydantic, Depends(get_curr_active_user)]):
    return current_user

# To populate the DB with sample data (run this separately or in a script)
def add_sample_users():
    db = SessionLocal()
    sample_users = [
        UserDB(username = "johnalice", full_name="John Smith", email="john_smith@example.com", password="secret"),
        UserDB(username="alice", full_name="Alice", email="alice@example.com", password="wonder", disabled=True),
    ]
    db.add_all(sample_users)
    db.commit()
    db.close()

#add_sample_users()
