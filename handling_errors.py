# Handling Errors
# source: https://fastapi.tiangolo.com/tutorial/handling-errors/

# There are many situations in which we need to notify an error to a client that is using our API.
# this client could be a:
    # browser with a frontend
    # a code from someone elsedescription
    # an IoT device etc

# We could need to tell the client that:
    # the client doesn't have enough privileges for that operation
    # The client doesn't have access to that resources
    # The item the client was trying to access doesn't exist. etc

# In these cases, we would normally return an HTTP status code in the range of 400 (from 400 499).

# This is similar to the 200 HTTP status codes (from, 200 to 299). 
# # The status codes in the 400 range mean that there was an error from the client.
# # 

# HTTPException
# # TO return HTTP responses with errors to the client to the client we use `HTTPException`

from fastapi import FastAPI, HTTPException
import logfire

app = FastAPI()
logfire.configure()
logfire.instrument_fastapi(app)

items = {"item1": "pen"}

@app.get('/items/{item_id}')
async def get_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}

# Raise an `HTTPException` in our code
'''
`HTTPException` is a normal Python exception wityh additional data relevant for APIs.
Because its a python exception, we don't `return` it , we `raise` it.
this also, means that if we are inside a utility function that we are calling inside our path operation function and we raise `HTTPException` from inside of that utility function, ti won't run the rest of the coe ein the path operation function, it will
terminate that request right awat and send the HTTP error from the `HTTPException` to the client.

The benefit of raising an exception over returning a value will be more evident in the section about "Dependencies and Security".

In the above example , when the client requests an item by an ID that doesn't exist, raise an exception with a status code of `404`.
'''

# note:; When raising an HTTPException, we can pass any value that can be converted to JSON as the parameter `detail`, not only `str`.
# we could pass a `dict`, a `list` etc.
# They are handled automatilcally by FastAPI and converted to JSON
#

# Add custom headers
# There are some situations in where it's useful to be able to add custom headers to the HTTP error. For instance, for some type of security 
# we probably won't need to use it directly in our code.
# but in case we needed it for an advanced scenario, we can add custom headers:


@app.get('/item-header/{item_id}/')
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-error": "There goes my error"},
        )
    return {"item": items[item_id]}


# # Install custom exception handlers
# source: https://fastapi.tiangolo.com/tutorial/handling-errors/#install-custom-exception-handlers
# We can add custom exception hadnlers with the same exception utilities from Startlette [: https://www.starlette.dev/exceptions/
# Let's say we have a custom exception `UnicornException` that we (or a library we use) might raise
# and we want to handle this exception globally with FastAPI
# we could add a custom exception handler with `@app.exception_handler()`:

from fastapi import Request
from fastapi.responses import JSONResponse

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name
    
@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={
            "message": f"Oops! {exc.name} did something. There goes a rainbow..."
        },
    )

@app.get('/unicorn/{name}')
async def read_unicorn(name: str):
    if name == 'yolo':
        raise UnicornException(name=name)
    return {
        "unicorn_name": name
    }


# Override the default exception handlers
# https://fastapi.tiangolo.com/tutorial/handling-errors/#override-the-default-exception-handlers
# # override request validation exceptions
# When a request contains invalid data, FastAPI internally raises a `RequestValidationError`
# and it also includes a default exception handler for it. 

# To override it, import the `RequstValidationError` and use it with `@app.exception_handler(RequestValidationError)` to decorate the exception handler
# The exception handler will receive a `Request` and the exception.

from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)

@app.get('/override-items/{item_id}')
async def view_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}

# RequestValidationError vs ValidationError(https://docs.pydantic.dev/latest/concepts/models/#error-handling)
'''
# # Warning 
# `RequestValidationError` is a sub-class of Pydantic's `ValidationError`.
# FastAPI uses it so that, if we use a Pydantic model in `response_model`, and our data has an error, we will see the error in our server log.

But the client/user will not see it. Insteadm the client will receive an "Internal Server Error" with an HTTP status code `500`.

It should be this way because if we have Pydantic `ValidationError` in our response or anywhere in our code (not in the client's request), it's actually a bug in our code.

and while we fix it, our clients/users shouldn't have access to internal information about the error, as that could expose a security vulnerability.
'''


# Use `RequestValidationError` body
# The `RequestValidationError` contains the `body` it received with invalid data
# We could use it while developing our app to log the body and debug it, return it ot the user etc.

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

@app.exception_handler(RequestValidationError)
async def validation_exception_handler_(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

class Student(BaseModel):
    id: int
    name: str

@app.post('/student/')
async def add_item(student: Student):
    return student

# FastAPI's HTTPException vs Starlette's HTTPException
# difference: FastAPI's `HTTPException` accespts any JSON-able data for the `detail` field, while Starlette's `HTTPException` only accepts strings for it.
# So, we can keep raising FastAPI's `HTTPException` as normnally in our code.
# But when we register an exception handler, we should register it for Starlette's `HTTPException`.

# This way, if any part of Starlette's internal code, or a Starlette extension or plug-in, raises a Starlette
# `HTTPException`, our handler will be able to catch and handle it.

# In this example, to be able to have both `HTTPException`s in the same coe, Starlette's exceptions is renamed to `StarletteHTTPException`:
'''
from startlette.exceptions import HTTPException as StartletteHTTPException
'''

# Reuse `FastAPI`s exception handlers
# If we want to use the exception along with the same default exception from `FastAPI`, we can import and reuse the default exception handlers from `fastapi.exception_handlers`:

from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)

@app.get('/reuse/items/{item_id}')
async def getting_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}




