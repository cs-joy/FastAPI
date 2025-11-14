# Query Parameter Models
# source: https://fastapi.tiangolo.com/tutorial/query-param-models/


# let's say, we have a grouypd of query parameters that are related, 
# we can creater a pydantic model to declare them
# This would allow us to re-use the model in multiple places and 
# also to declare validations and metadata for all the parameters 
# ar once.


# delcvare the parameters that we need in a pydantic model, and then delcare the parameter as Query:
from fastapi import FastAPI, Query
import logfire
from pydantic import BaseModel, Field
from typing import Annotated, Literal

app = FastAPI(title="Query Parameter and Models")
logfire.configure()
logfire.instrument_fastapi(app)


class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

@app.get('/items/')
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query

class FilterParams_with_Annotated(BaseModel):
    limit: Annotated[int, Field(55, gt=0, le=55)]
    offset: Annotated[int, Field(-6, ge=-6)]
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

@app.get('/items-annotated/')
async def view_items(filter_query_ann: Annotated[FilterParams_with_Annotated, Query()]):
    return filter_query_ann


# Forbid Extra Query Parameters
## in some special use cases (probably not very common), we might want to restrict the query parametes that we want ti receive.
# we can use pydantic model configuration to `forbid` any `extra` fields:

class Library(BaseModel):
    model_config = {"extra": "forbid"}

    limit: Annotated[int, Field(100, gt=0, le=100)]
    offset: Annotated[int, Field(0, ge=0)]
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

@app.get('/library/')
async def view_library(filter_query: Annotated[Library, Query()]):
    return filter_query

'''
If a client tries to send some extra data in the query parameters, they will receive an error response
'''

# Spoiler alert: we can also use pydantc models to declare cookies ad headers, but you will read about that later in the tutorial

