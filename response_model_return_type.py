# Response Model - Return Type
# source: https://fastapi.tiangolo.com/tutorial/response-model/

# We can declare the type used for the response by annotating the path operation function return type.

# We can use the type annotations the same way we would for input data in function parameters, we can use Pydantic models, lists, dictionaries, scalar values like integers, booleans etc.

from uuid import UUID
import logfire
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
logfire.configure()
logfire.instrument_fastapi(app)

class Product(BaseModel):
    id: UUID | None = None
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []

store: list[Product] = []

@app.post('/products/')
async def create_product(product: Product) -> Product:
    store.append(product)
    return product

@app.get('/products/')
async def view_product() -> list[Product]:
    return store

'''

FastAPI will use this return type to:
- Validate the returned data
- Add a JSON Schema for the response, in the OpenAPI path operation

But most importantly:
- It will limit and filter the output data to whats is defined in the return type
    - this is particularly important for security
'''

# `response_model` parameter
# source: https://fastapi.tiangolo.com/tutorial/response-model/#response-model-parameter
'''
there are some cases where we need or want to return some data that is not exactly what the 
type declares.

for example, we could want to return a dictionary or a database object but declare it as a 
Pydantic Model. This way the Pydantic model would do all the data documentation, validation, etc. 
for the object that we returned (e.g., a dictionary or database object).

if we added the return type annotation, tools and editors would complain with a (correct) error 
telling us that our functions is returning type (e.g., dict) that is different from what we 
declared (e.g., Pydantic model).

In those cases, we can use the path operation decorator parameter `response_model` instead 
of return type.

# We can use the `response_model` parameter in any of the path operations:
- @app.get()
- @app.post()
- @app.put()
- @app.delete()
etc
'''
from typing import Any

class Phone(BaseModel):
    name: str
    description: str | None = None
    brand: str
    model: str
    price: float
    tax: float | None = None
    tags: list[str] = []

@app.post('/phone/', response_model=Phone)
async def add_phone(phone: Phone) -> Any:
    return phone

@app.get('/phone/', response_model=list[Phone])
async def view_phone() -> Any:
    return [
        {"name": "Samsung A50s", "brand": "Samsung", "model": "A50s", "price": 195.98},
        {"name": "iPhone 13", "brand": "Apple", "model": "13", "price": 387.56}
    ]

# Note: `response_model` parameter is a parameter of the "decorator" method(get, post, put and so on)


# `response_model` Priority
# source: https://fastapi.tiangolo.com/tutorial/response-model/#response-model-priority
# if we declare both a return type and a `response_model`, the `response_model` will take priority and be used by FastAPI

# This way we can add correct type annotations to our functions even when we are returning a type different than the response model, to be
# used by the editor and tools like mypy. 

# we can also use `response_model=None` to disable creating a response model for that path operation, we might need to do
# if we are adding type annotations for things that are not valid Pydantic field

# Return the same input data
# Here we are declaring a `UserIn` model, it will contain a plaintext password.

from pydantic import EmailStr

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

user_list: list[UserIn] = []

# Don't do this in production!
@app.post('/user/')
async def create_user(user: UserIn) -> UserIn:
    user_list.append(user)
    return user

'''
Now, whenever a browser is creating a user with a passwordm the API will return the same password in the response.
in this case, it might not be a problem, because it's the same user sending the password.
But if we use the same model for another path operation, we could be sending our user's password to every client.

# Danger:
Never store the plain password of a user or send it in a response like this, unless you know all the caveats and you know what are you doing.
'''
# Add an output model
# # we can instead create an input model with the plaintext password and an output model without it.

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

@app.post('/add-an-output-model/', response_model=UserOut)
async def add_user(user: UserIn) -> Any:
    return user

# So, FastAPI will take care of filtering out all the data that is not declard in he output model (using Pydantic).

# `response_model` or Return type
# In this case, because the two models are different, if we annotated the function return type as `UserOut`, the editor and tools would
# complain that we are returning an invalid type, asd those are differnt classes.
'''
@app.post('/add-an-output-model/')
async def add_user(user: UserIn) -> UserOut:
    return user

note: this will generate an error
'''

# that's why in this example we have to declare it in the `response_model` parameter.

# # Return type and Data Filtering
# source: https://fastapi.tiangolo.com/tutorial/response-model/#return-type-and-data-filtering
# Let's continue from the previous example. We wanted to annotate the function with one type, but we wanted to be able to
# return from the function something that actually includes more data.

# We want FastAPI to keep filtering the data using the response model. So that even though the function returns more data,
# the response will onclie include the fileds declared in the response model.

# In the previous example, because the classes were different, we had to use the `response_model` parameter. But that also means that we don't get the support from the editor and tools checking the function return type.
# But in most of the cases where we need to do something like this, we want the model just filter/remove some of the data as in this example.

# And in those cases,we can use classess and inheritance to take advantages of function type annotations to get better suppirt in the editor and tools, and still get the FastAPI data filtering.


class BaseUserProfile(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserProfile(BaseUserProfile):
    password: str

@app.post('/return-type-and-data-filtering/')
async def new_user(user: UserProfile) -> BaseUserProfile:
    return user

# With this, we get tooling support, from editors and mypy as this code is correct inm terms of types, but we also get the data filtering from FastAPI


# Other Return Type Annotations
# source: https://fastapi.tiangolo.com/tutorial/response-model/#other-return-type-annotations

# Return a Response Directly
# advance docs: https://fastapi.tiangolo.com/advanced/response-directly/

from fastapi import Response
from fastapi.responses import JSONResponse, RedirectResponse

@app.get('/portal/')
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return JSONResponse(content={"message": "Here's your interdimensional portal."})

# Annotate a Response Subclass
# We can also use a subclass of `Response` in the type annotation:

@app.get('/teleport')
async def get_teleport() -> RedirectResponse:
    return RedirectResponse(url="https://www.youtube.com/watch?v=9kLMrzhGc5g")

# This will also work because `RedirectResponse` is a subclass of `Response`, and FastAPI will automatically handle this simple case

# Invalid Return Type Annotations
# source: https://fastapi.tiangolo.com/tutorial/response-model/#invalid-return-type-annotations

@app.get('/invalid-return-type-annotations')
async def test(teleport: bool = False) -> Response | dict:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return {"message": "Here's your interdimensional portal."}

# ... this failes because the type annotation is not a Pydantic type and is not just a single `Response` class or subclass, it's a union (any of the two)
# between a `Response` and a `dict`.

# Disable Response Model
# ....
# TODO

