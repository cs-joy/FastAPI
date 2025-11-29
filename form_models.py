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


