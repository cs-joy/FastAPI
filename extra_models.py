# Extra Models
# source: https://fastapi.tiangolo.com/tutorial/extra-models/

# It will be common to have a more than one related model.

# This us especially the case for user models, because:
'''
- The inout model needs to be able to have a password.
- The output model should not have a password.
- The database model would probably need to have a hashed password.
'''


# note: about security: https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/


# Multiple models

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
import logfire

app = FastAPI()
logfire.configure()
logfire.instrument_fastapi(app)

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_namel: str | None = None

def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
    print(f'user_in.model_dump(): {user_in.model_dump()}')
    # print(f'UserInDB(**user_in.model_dump()): {UserInDB(**user_in.model_dump())}')
    print('User saved! ... not really')
    return user_in_db


@app.post('/user/', response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved


# Unpacking a `dict`
# If we take a `dict` like `user_dict` and pass it to a function (or class)
#  with `**user_dict`, Python will "unpack it". it will pass the keys and 
#  values of the `user_dict` directly as key-value arguments.

# or more exactly, using `user_dict` directly, with whatever contents it might have in the future:
'''
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"]
)
'''

# A pydantic model from the contents of another: https://fastapi.tiangolo.com/tutorial/extra-models/#a-pydantic-model-from-the-contents-of-another



# Note: the supporting additional functions `fake_password_hasher` and `fake_save_user` are just demo a possible flow of the data, but they of course are not providing any real security


# Reduce duplication :https://fastapi.tiangolo.com/tutorial/extra-models/#reduce-duplication

# Reducing code duplication is one of the core ideas in FastAPI

# AS code duplication increements the chances of
        # bugs
        # security issues
        # code desynchronization issues (when we update in one place but not in the others)

# And these models are all sharing a lot of the data and duplicating attribute names and types

# # We could do better.
# We can declare a `UserBase` model that serves as a base for our other models. And then we can make subclasses of that model that inherit its attributes (type declarations, validation etc).
# All the data conversion, validation, documentation , etc. will still work as normally.

# That way, we can declare just the differences between the models (with plaintext `password`, with `hashed_pasword` and without password):


class StudentBase(BaseModel):
    student_id: str
    username: str
    email: EmailStr
    department: str
    full_name: str | None = None

class StudentIn(StudentBase):
    password: str

class StudentOut(StudentBase):
    pass

class StudentInDB(StudentBase):
    hashed_password: str

def fake_password_hasher_2(raw_password: str) -> str:
    return "secret" + raw_password

def fake_save_user_in_db(student_in: StudentIn):
    hashed_password = fake_password_hasher_2(student_in.password)
    student_in_db = StudentInDB(**student_in.model_dump(), hashed_password=hashed_password)
    print('User saved! ..not really')
    return student_in_db

@app.post('/student', response_model=StudentOut)
async def create_student(student_in: StudentIn):
    student_saved = fake_save_user_in_db(student_in)
    return student_saved

# `Union` or anyOf`
# We can declare a response to be the `Union` of two or more types, that means that the response would be any of them
# it will be defined in OpenAPI with `anyOf`

'''
note: 
when defining a `Union`, include the most specific type first, 
followed by the less specific type. In the example bellow, 
the more specific `PlaneItem` comes before `CarItem` in `Union[PlaneItem, CarItem]`.
'''
from typing import Union

class BaseItem(BaseModel):
    description: str
    type: str

class CarItem(BaseItem):
    type: str = "car"

class PlaneItem(BaseItem):
    type: str = "plane"
    size: int

items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "aeroplane",
        "type": "plane",
        "size": 5
    }
}

@app.get('/items/{item_id}', response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]

# note: https://fastapi.tiangolo.com/tutorial/extra-models/#union-in-python-3-10
# look at the swagger docs(localhost:8000/docs) at response schama. To understand effect of the Union[PlaneItem, CarItem] or Union[CarItem, PlaneItem] (change accordingly)

# List of models
# The same way, we can declare responses of lists of objects.
class Rubisq(BaseModel):
    name: str
    description: str

rubisq = [
    {"name": "Foo", "description": "a nice a rubisq"},
    {"name": "Bar", "description": "it's my rubisq"},
]

@app.get('/rubisq/', response_model=list[Rubisq])
async def view_rubisq():
    return rubisq


# Response with arbitrary `dict`
# # We can also declare a response using a plain arbitrary `dict`, declaring jsut the type of the keys and values, without using pydantic model.
# # This is userful if we don't know the valid field/]attribute names (that would be needed for a Pydantic model) beforehand.
@app.get('/keyword-weights/', response_model=dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}

# Recap:::
'''
Use multiple pydantic models and inherit freely for each case.

WE don't need to have a single data model per entity if that entity must be able to have different "states". As the case with the user "entity" with a state including
`password`, `password_hash` and no password.
'''
