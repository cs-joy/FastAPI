# Form Data
# source: https://fastapi.tiangolo.com/tutorial/request-forms/

# # When we need to receive form fields instead of JSON, we can use `Form`

### requirement to use `Form`
# install `python-multipart`

from fastapi import FastAPI, Form
from typing import Annotated
import logfire

app = FastAPI()
logfire.configure()
logfire.instrument_fastapi(app)


@app.post('/login/')
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return username

# for instance, in one of the ways the OAuth2 specification can be used (called "password flow") it is required to send a `username` and `password` as form fields.
# the specification requires the fields to be exactly named `username` amd `password`, and to be sent as form fields, not JSON.
# With `Form` we can declare the same configurations as with `Body` (and `Query`, `Path`, `Cookie`), including validation, examples an alias (e.g., `user-name` instead of `username`), etc.

# `Form` is inherits directly from `Body`
# To declare form bodies, we need to use `Form` explicitly, because without it the parameters would be interpreted as query parameters or body (JSON) parameters.

# About "Form Fields"
'''
Data from forms is normally encoded using the "media type" application/x-www-form-urlencoded.

But when the form includes files, it is encoded as multipart/form-data. You'll read about handling files in the next chapter.

read more: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST
'''



'''
Warning!
We can declare multiple `Form` parameters in a path operation, but we can't also declare
`Body` fields that we expect to receive as JSON, as the request will have the body
encoded using `application/x-www-form-urlencoded` instead of `application/json`.

this is a limitation of HTTP protocol not just FastAPI
'''
# let's see...

from fastapi import Body
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    tax: float = 0.58


@app.post('/new/login/')
async def limitation_check(username: Annotated[str, Form()], password: Annotated[str, Form()], body_field: Annotated[Item, Body()]):
    result = {
        "username": username,
        "password": password,
        "body_field": body_field
    }
    return result

