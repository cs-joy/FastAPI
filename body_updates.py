# Body Updates
# source: https://fastapi.tiangolo.com/tutorial/body-updates/

# # Update replacing with `PUT`
# to udpate an item we can use the `HTTP PUT` operation.
# We can use the `jsonable_encoder` to convert the input data to data that can be stored as JSON (e.g., with a NonSQL database)
# For example, converting `datetime` to `str`.


from fastapi import FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import logfire

app = FastAPI()
logfire.configure()
logfire.instrument_fastapi(app)

class Product(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 1.032
    tags: list[str] = []


products = {
    "p1": {
        "name": "Graphics Card",
        "price": 1203.21,
    },
    "p2": {
        "name": "Mouse",
        "description": "Wireless mouse",
        "price": 15.94,
        "tax": 4.49,
    },
    "p3": {
        "name": "Keyboard",
        "description": None,
        "price": 5.99,
        "tax": 1.11,
        "tags": [],
    }
}

@app.get('/products/{product_id}/')
async def view_item(product_id: str):
    is_found = False
    is_found = any(product_id == pk for pk in products.keys())
    if is_found:
        return products[product_id]
    raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found!')

@app.put('/products/{product_id}/', response_model= Product)
async def update_product_info(product_id: str, product: Product):
    is_found = False
    is_found = any(product_id == pk for pk in products.keys())
    if is_found:
        update_product_encoded = jsonable_encoder(product)
        products[product_id] = update_product_encoded
        return update_product_encoded
    raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found!')

# `PUT` is used to receive data that should replace that existing data.

# Warning about replacing
# source: https://fastapi.tiangolo.com/tutorial/body-updates/#warning-about-replacing
# ..... 

# # Partial updates with `PATCH`
# We can also use the `HTTP PATCH` operation to partially update data.
# This means that we can send only the data we want to update, leaving the rest intact.

# # Using Pydantic's `excluding_unset` parameter _> https://fastapi.tiangolo.com/tutorial/body-updates/#using-pydantics-exclude-unset-parameter
# If we want to receive partial updates, it's very useful to use the parameter `exclude_unset` in Pydantic's models `.model_dump()`.
# Like `product.model_dump(excluding_unset=True)`
# That would generate a `dict` with only the data that was set when creating the `product` model, excluding default values.
# Then we can use this to generate a `dict` with only the data that was set (send in the request), omitting default values:

@app.patch('/product/{product_id}', response_model=Product)
async def udpate_product(product_id: str, product: Product):
    is_product_exist = False
    is_product_exist = any(product_id == pk for pk in products.keys())
    if is_product_exist:
        stored_product_data = products[product_id]
        stored_product_model = Product(**stored_product_data)
        update_data = product.model_dump(exclude_unset=True)
        updated_product = stored_product_model.model_copy(update=update_data)
        products[product_id] = jsonable_encoder(updated_product)
        return updated_product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Not Found!")

# Partial Updates recap
'''
In summary, to apply partial updates we would:
- (Optionallly) use `PATCH` instead of `PUT`
- retrieve the stored data
- put that data in a pydantic model
- generate a `dict` without default values from the input model (using `excluding_unset`).
    - this way we can update only the values actually set by the user, instaed of override values already stored with default values in our model.
- create a copy of the stored model, updating its attributes with the received partial updates (using the `update` parameter)
- convert the copied model to something that can be stored in our DB (for example, using the `jsonable_encoder`).
    - this is comparable to using the model's `.model_dump()` method again, but it makes sure (and converts) the values to data types that can be converted to JSON, for example, `datetime` to `str`.
- save the data in our DB
- return the updated model
'''

# :::Tip:::
# We can actually use this same technique with an HTTP `PUT` operation.

# Note::
# Notice that the input model is still validated. 
# So, if we want to receive partial updates that can omit all the attributes, we need to have a model with all the attributes marked as optional (with default values or `None`)
# To distinguish from the models with all optional vlaues for "updates" and models with required values for "creation", we can use the ideas described in "Extra Models: https://fastapi.tiangolo.com/tutorial/extra-models/"
