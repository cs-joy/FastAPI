## Query Parameters:
# source: https://fastapi.tiangolo.com/tutorial/query-params/
# when we declare a function parameters that are not part of the path
# parameters, they are automatically interpreted as `query` parameters

from fastapi import FastAPI

app = FastAPI()

fake_items_db = [
    {"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}
]

@app.get('/items')
async def read_fake_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

# the query is the set of key-value pairs thats go after the `?` in a URL, separated by `&` characters.
# for instance, http://localhost:8000/items?skip=0&limit=10
#            ...the query parameters are:
#               - skip: with a value of 0
#               - limit: with a value of 10


## Optional Parameters
# Optional query parametersm by setting their default to `None`:
@app.get('/items/{item_id}')
async def read_item(item_id: str, q: str | None = None): # item_id -> path parameter, q-> query parameter
    if q:
        return {
            "item_id": item_id,
            "q": q
        }
    return {
        "item_id": item_id
    }

## Query parameter type conversion
# we can also declare `bool` types, and they will be converted:
@app.get('/items/qc/{item_id}')
async def read_item_qc(item_id: str, q: str | None = None, short: bool = False):
    item = {
        "item_id": item_id
    }
    if q:
        item.update({
            "q": q
        })
    if not short:
        item.update({
            "description": "This is an amazing item that has a long desciption"
        })
    return item

## Multiple path and query parameters
# don't need to declare the query parameters in any specific order
# they will be detected by name:
@app.get('/users/{user_id}/items/{item_id}')
async def read_user_item_(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {
        "item_id": item_id,
        "owner_id": user_id
    }
    if q:
        item.update({"q": q})
    if not short:
        item.update({
            "description": "This is an amazing item that has a long description"
        })
    return item

## Required query parameters
# to make a query parameters is required just ignore to set any default value, e.g., None
@app.get('/product/{product_id}')
async def read_user_product(product_id: str, needy: str):
    item = {
        "product_id": product_id,
        "needy": needy
    }
    return item

# here the query parameter `needy` is a required query parameter of type `str`.


# # #
# we can also define some parameters as required, some as having a default valu, some entirely optional
@app.get('/products/{product_id}')
async def view_user_product(
    product_id: str,
    needy: str,
    skip: int = 0,
    limit: int | None = None
):
    product = {
        "product_id": product_id,
        "needy": needy,
        "skip": skip,
        "limit": limit
    }
    return product








