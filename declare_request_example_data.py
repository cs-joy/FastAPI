# Declare Request Example Data
# # source: https://fastapi.tiangolo.com/tutorial/schema-extra-example/

# We can declare examples of the data of our app can receive. Here are several ways to do it.

from fastapi import FastAPI
from pydantic import BaseModel
import logfire


app = FastAPI()
logfire.configure()
logfire.instrument_fastapi(app)

# Extra JSON Schema data in Pydantic models
# we can declare `examples` for a Pydantic model that will be added to the generated JSON Schema.
#

class Surah(BaseModel):
    name: str
    description: str
    revealed: str
    surah_no: int
    ayah: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Sura Al-Fatiha",
                    "description": "First Sura of Al-Quran",
                    "revealed": "Meccan",
                    "surah_no": 1,
                    "ayah": 7,
                },
                {
                    "example_2": "value_2"
                }
            ],
            "extra_info": [
                {
                    "tag": "checking",
                    "about": "info about the attrbutes/class",
                }
            ]
        }
    }


@app.put('/al-quran/{surah_no}')
async def update_surah_profile(surah_no: int, surah: Surah):
    profile = {"surah_no": surah_no, "surah": surah}
    return profile

# That extra info will be added as-is to the output JSON Schema for that model, and it will be used in the API docs.
# In pydantic version 2, we would use the attribute `model_config`, that takes a `dict` as described in
# Pydantic's docs" COnfiguration: https://docs.pydantic.dev/latest/api/config/
# We can set `json_schema_extra` with `dict` containing any additional data we would like to show up in the generated JSON Schema, inlcuding `examples`.

# tip
# # we could use the same technique to extend the JSON Schema and add our own custom extra info.
# # for example, we could use it to add metadata for a frontend user interface, etc.


#################################################

# `Field` additional arguments
# When using `Field() with Pydantic models, we can also declare addtional `examples`:
from pydantic import Field

class Tree(BaseModel):
    name: str = Field(examples=["Foo"])
    description: str | None = Field(default=None, examples=["A very nice Tree"])
    age: float = Field(examples=[0.5])
    price: float = Field(examples=[122.30])
    tax: float | None = Field(default=None, examples=[1.64])

@app.put('/tree/{tree_id}')
async def updated_tree_info(tree_id: int, tree: Tree):
    results = {"tree_id": tree_id, "tree": tree}
    return results

# # # `examples` in JSON Schema - OpenAPI
'''
When using any of:
- Path()
- Query()
- Header()
- Cookie()
- Body()
- Form()
- File()

# We can also declare a group of `examples` with additional information that will be added to their JSON Schemas inside of OpenAPI.
'''

# `Body` with examples
from typing import Annotated
from fastapi import Body

class Pen(BaseModel):
    name: str
    description: str | None = None
    price: float
    color: str
    tax: float | None = None

@app.put('/pen/{item_id}')
async def udpate_pen_item(
    item_id: int, 
    item: Annotated[Pen, Body(
        examples= [
            {
                "name": "Matador Orbit",
                "description": "matador pen",
                "price": 1.1,
                "color": "blue",
                "tax": "0.001"
            }
        ]
    )]
):
    results = {"item_id": item_id, "item": item}
    return results


# # # # # 
# # `Body` with multiple `examples`
# we can of course also pass multiple `examples`:
class AirConditioner(BaseModel):
    brand_name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.put('/ac/{item_id}')
async def update_item_ac(
    *,
    item_id: int,
    item: Annotated[AirConditioner, Body(
        examples= [
            {
                "brand_name": "Midea Inverter",
                "description": "ac",
                "price": 105.84,
                "tax": 16.81
            },
            {
                "name": "Walton AC",
                "price": 89.451
            },
            {
                "name": "Singer AC",
                "price": "thirty five thousand and two hundred fifty"
            }
        ]
    )]
):
    results = {"item_id": item_id, "item": item}
    return results

'''
When you do this, the examples will be part of the internal JSON Schema for that body data.

Nevertheless, at the time of writing this, Swagger UI, the tool in charge of showing the docs UI, 
doesn't support showing multiple examples for the data in JSON Schema. But read below for a workaround.
'''


#######################################
# # OpenAPI-specific `examples`
# https://fastapi.tiangolo.com/tutorial/schema-extra-example/#openapi-specific-examples


# Using the `openapi_examples` Parameter
# We can declare the OpenAPI-specific `examples` in FastAPI with the parameter `openapi_examples` for: 
# Path()
# Query()
# Header()
# Cookie()
# Body()
# Form()
# File()

# The keys of the `dict` identify each example, and each value is another `dict`.

# Each specific example `dict` in the `examples` can contain:
'''
- summary: Short description for the example
- description: A long description that can contain Markdown text
- value: This is the actual example shown, e.g., `dict`.
- externalValue: alternative to `value`, a URL pointing to the example. Although this might not be supported by as many tool as value.
'''

class Phone(BaseModel):
    name: str
    description: str | None = None
    brand: str
    price: float
    tax: float | None = None

@app.put('/phone/{mobile_id}')
async def update_item(
    *,
    mobile_id: int,
    item: Annotated[
        Phone, Body(
            openapi_examples= {
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** works correctly.",
                    "value": {
                        "name": "Samsung A50",
                        "description": "An Android Phone",
                        "brand": "Samsung",
                        "price": 45.82,
                        "tax": 4.384,
                    },
                },
                "converted": {
                    "summary": "An example with converted data",
                    "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                    "value": {
                        "name": "Vivo Y27s",
                        "brand": "Vivo",
                        "price": 24.78,
                    },
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "name": "Google Pixel Phone",
                        "brand": "G61",
                        "price": "thirty five point four",
                    },
                },
            },
        ),
    ],
):
    results = {"mobile_id": mobile_id, "item": item}
    return results

# # # # Technical Details
# https://fastapi.tiangolo.com/tutorial/schema-extra-example/#technical-details
# note: This old OpenAPI-specific `examples` parameter is now `openapi_examples` since fastAPI v0.103.0


# # # JSON Schema's `examples` fields
# https://fastapi.tiangolo.com/tutorial/schema-extra-example/#json-schemas-examples-field


# # Pydantic and FastAPI examples
# https://fastapi.tiangolo.com/tutorial/schema-extra-example/#pydantic-and-fastapi-examples


