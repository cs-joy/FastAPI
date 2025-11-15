
# Body Fields
# source: https://fastapi.tiangolo.com/tutorial/body-fields/
# 
## The same we can declare additional validation and metadata in path operation function parameters with `Query`, `Path` and
# `Body`, we can declare validation and metadata inside of Pydantic models using Pydantic's `Field`.
from fastapi import FastAPI, Body, Path, Query
from typing import Annotated
from pydantic import BaseModel, Field
import logfire


app = FastAPI()
logfire.configure()
logfire.instrument_fastapi(app)


# Declare model attributes
# we can use `Field` with model attributes:
class Product(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the product", max_length=300
    )
    price: float = Field(gt=0, description="the price must be greater than zero")
    tax: float | None = None

@app.put('/product/{product_id}')
async def update_product(product_id: int, product: Annotated[Product, Body(embed=True)]):
    results = {"product_id": product_id, "product": product}
    return results

# note: `Field` works the same way as `Query`, `Path` and `Body`, it has all the same parameters etc

'''
# Technical details
Actually, `Query`, `Path` and others we will see next create objects of subclcasses of a commont `Param` class, which itself a subclass of Pydantic's
`FieldInfo` class.
And Pydantic's `Field` return an instance of `FieldInfo` class.
`Body` also retuns objec ts of a subclass of `FieldInfo` directly. And there are others we will see later thats are subclass of the `Body` class.
Remember that when we imprt `Query`, `Path` and others from `fastapi`, those are actually frunctions that return special classes.
'''


# Recap
## WE can use Pydantic's `Field` to declare extra validations and metadata for model attributes.
## WE we can also use the extra keyword arguments to pass additional JSON Scheme metadata