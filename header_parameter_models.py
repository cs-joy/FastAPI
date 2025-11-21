# Cookie Parameter Models
# source: https://fastapi.tiangolo.com/tutorial/header-param-models/

# If we have a group of related header parameters, we can create a Pydantic model to delcare them.
# this would allows us to re-use the model in multiple places and also to declare validations and metadata for all the parameters at once

from typing import Annotated
from fastapi import FastAPI, Header
import logfire
from pydantic import BaseModel

app = FastAPI()
logfire.configure()
logfire.instrument_fastapi(app)

class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []

@app.get('/items/')
async def header_parameter_model(headers: Annotated[CommonHeaders, Header()]):
    return headers

'''
FastAPI will extract the data for each field from the headers in the request and give you the Pydantic model you defined.
'''

# Forbid Extra Headers
# In some special user cases (probably not very common), you might want to restrict the headers that you want to receive
# we can use pydantic model configuration to `forbid` any `extra` fields.

class ForbidExtraHeader(BaseModel):
    model_config = {"extra": "forbid"}

    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []

@app.get('/forbid/')
async def forbid_extra_headers(headers: Annotated[ForbidExtraHeader, Header()]):
    return headers

# when a client tries to send some extra headers, they will receive an error response.

# For instance, if the client tries to send a `engine` header with a value of `sql`, they will receive an error response telling them that the header parameter `engine` is not allowed.
'''
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["header", "engine"],
            "msg": "Extra inputs are not permitted",
            "input": "sql",
        }
    ]
}
'''

# Disable convert underscore
# The same way as with regular header parameters, when we have underscore character in the parameter names, they are automatically converted to hyphens.

# For example, if we have a header parameter `save_data`in the code, the expected HTTP header will be `save-data`,
# and it will show up like that in the docs.

# if for some reason we need to disable this automatic conversaion, we can do it as well for pydantic models for header parameters.

class DisableConevertUnderscore(BaseModel):
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []


@app.get('/disable-convert-underscore/')
async def disable_convert_underscore(headers: Annotated[DisableConevertUnderscore, Header(convert_underscores=False)]):
    return headers


# Before setting `convert_underscores` to `False`, keep in mind that some HTTP proxies and servers disallow the usage of headers with underscores.