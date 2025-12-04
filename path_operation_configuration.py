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


# Description from docstring
'''
As description tend to be long and cover multiple lines, we can declare the path operation description
in the function `docstring` and FastAPI will read it from there.

We can write Markdown in the docstring, it will be interpreted and displayed correctly (taking into account docstring indentation).
'''

@app.post('/prod/', response_model=Product, summary="Summary of a product")
async def init_product(product: Product):
    """
    Create a product with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have `tax`, we can omit this
    - **tags**: a set of unique tag strings for this product
    """
    return product
    

# Response description
# We can specify the response description with the parameter `response_description`:
@app.post('/response-description/', response_model=Product, summary="Create an item", response_description="The created item")
async def response_description(product: Product):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return product


# Deprecate a path operation
# If we need to mark a path operation as "deprecated", but without removing it, pass the parameter `derecated`:

@app.get('/deprecated-path-operation/accessories/', tags=["accessories"])
async def view_items():
    return [
        {
            "name": "Foo",
            "price": 48,
        }
    ]

@app.get('/deprecated-path-operation/categories/', tags=["categories"])
async def read_categories():
    return [
        {
            "category1": "technology"
        }
    ]

@app.get('/deprecated-path-operation/categories/elements/', tags=["elements"], deprecated=True)
async def get_deprecated_elements():
    return [
        {
            "item_id": "423m5294nsd724nf"
        }
    ]

