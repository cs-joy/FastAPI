# Path Operation Configuration
# source: https://fastapi.tiangolo.com/tutorial/path-operation-configuration/

# There are several parameters that we can pass to our path operation decorator to configure it.
# note:: These parameters are passed directly to the path operation decorator, not to our path operation function.

# # Respone Status Code
'''
We can define the (HTTP) `status_code` to be used in the response of our path operation.
We can pass directly the `int` code, like `404`.
But if we don't remember what each number code is for, we can use the shortcut constants in `status`:
'''
from fastapi import FastAPI, status
import logfire
from pydantic import BaseModel

app = FastAPI()
logfire.configure()
logfire.instrument_fastapi(app)

class Product(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()

@app.post('/product/', response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: Product):
    return product


# # Tags
# We can add tags to our path operation, pass the parameter `tags` with a `list` of `str` (commonly just one `str`)

@app.post('/products/tags/', response_model=Product, tags=["products"], status_code=status.HTTP_201_CREATED)
async def add_product(product: Product):
    return product

@app.get('/products/tags/', tags=["products"])
async def view_item():
    return [
        {
            "name": "Foo",
            "price": 43.21,
        }
    ]

@app.get('/users/product/', tags=["users"])
async def get_users():
    return [
        {
            "username": "johndoe"
        }
    ]


# # Tags with Enum
# if we have a big application, we might end up accumulating several tags, and we would want to make sure we always use the same tag for related path operations.

# In these cases, it could make sense to store the tags in an `Enum`.

from enum import Enum

class Tags(Enum):
    items = "products"
    users = "users"

@app.get('/enum/products/', tags=[Tags.items])
async def get_items():
    return [
        "Portal gun", "Plumbus"
    ]

@app.get('/enum/users/', tags=[Tags.users])
async def read_users():
    return [
        "Rick",
        "Morty"
    ]


# # Summary and Description
# We can add a `summary` and `description`:
@app.post(
    '/summary/description/',
    summary='Create an item',
    description='Create an item with all the information, name, description , etc'
)
async def create_item(product: Product):
    return product



