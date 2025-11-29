# Form Models

# source: https://fastapi.tiangolo.com/tutorial/request-form-models/

# Pydantic Models for Forms

from typing import Annotated
from fastapi import FastAPI, Form
from pydantic import BaseModel
import logfire


app = FastAPI()
logfire.configure()
logfire.instrument_fastapi(app)

class FormData(BaseModel):
    username: str
    password: str


@app.post('/login/')
async def login(data: Annotated[FormData, Form()]):
    return data


# Forbid Extra Form Fields
# # In some special uses cases (probably not very common), we might want to restrict the form fields to only those declared in the Pydantic model. and forbid any extra fields

# to do that,
class FormInfo(BaseModel):
    username: str
    password: str
    model_config = {"extra": "forbid"}

@app.post('/login/forbid/')
async def sign_in(data: Annotated[FormInfo, Form()]):
    return data








