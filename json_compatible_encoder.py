# JSON Compatible Encoder
# source: https://fastapi.tiangolo.com/tutorial/encoder/

'''
There are some cases where we might need to convert a data type (like a Pydantic model) to something compatible with JSON
(like a `dict`, `list`, etc.)

For instance, if we need to store it ina database.

For that, FastAPI provides a `jsonable_encoder()` function.
'''

# Using the `jsonable_encoder`
# Let's imagine that we have a database `fake_db` that only receives JSON compatible data.
# For instance, it doesn't receive `dateitem` objects, as those are not compatible with JSON.
# So, a `dateitem` object would have to be converted to a `str` containing the data in "ISO format".
# The same way, this database wouldn't receive a Pydantic model (an object with attributes), only a `dict`
# In that case, we can use `jsonable_encoder` format. It receives an object, like a Pydantic model, and returns a JSON compatible version.


from fastapi import FastAPI
import logfire
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from datetime import datetime

app = FastAPI()
logfire.configure()
logfire.instrument_fastapi(app)

fake_db = {}

class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None

@app.put('/items/{id}')
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data

    return {
        "status": "success",
        "data": fake_db,
    }

'''
In this example, it would convert the Pydantic model to a dict, and the datetime to a str.

The result of calling it is something that can be encoded with the Python standard json.dumps().

It doesn't return a large str containing the data in JSON format (as a string). It returns a Python standard data structure (e.g. a dict) with values and sub-values that are all compatible with JSON
'''