# Body - Nested Models
# source: https://fastapi.tiangolo.com/tutorial/body-nested-models/

# With FastAPI, we can 
                        # define
                        # validate
                        # document and 
                        # use arbitrarily deeply nested models

from pydantic import BaseModel
from fastapi import FastAPI
import logfire

app = FastAPI()
logfire.configure()
logfire.instrument_fastapi(app)

class Product(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list = []


# # List Fields

@app.put('/list-fields/{item_id}')
async def update_item(item_id: int, item: Product):
    results = {"litem_id": item_id, "item": item}
    return results
# so, `tags` be a list, although it doesn't declare the type of the elements of the list.


# # List fields with type parameter
# python has a specific way to declare lists with internal types, or "type parameter":
# # Import typing's `List`
'''
python3.8+
------------------------------------
from typing import List, Union
from fastapi import fastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: List[str] = []
'''
# python 3.10+
# we have python 3.12

class Todo(BaseModel):
    serial: int
    date: str
    time: str | None = None
    topic: list[str] = []
    total_spending_time_on_the_topic: dict | None = None

@app.put('/todo/{name}')
async def todo_daily(name: str, routine: Todo):
    profile = {
        "name": name,
        "routine": routine
    }

    return profile

'''
request:::::
--------------
path paramter value, $name = joy
{
  "serial": 1,
  "date": "15_november",
  "time": "08:15 AM",
  "topic": ["Machine Learning", "GraphQL", "Kubernetes", "Docker"],
  "total_spending_time_on_the_topic": {
       "Machine Learning": "1.16 Hours",
       "GraphQL": "2.11 Hours",
       "Kubernetes": "3.30 Hours",
       "Docker": "1.49 Hours"
   }
}


response:::::
-------------
{
  "name": "joy",
  "routine": {
    "serial": 1,
    "date": "15_november",
    "time": "08:15 AM",
    "topic": [
      "Machine Learning",
      "GraphQL",
      "Kubernetes",
      "Docker"
    ],
    "total_spending_time_on_the_topic": {
      "Machine Learning": "1.16 Hours",
      "GraphQL": "2.11 Hours",
      "Kubernetes": "3.30 Hours",
      "Docker": "1.49 Hours"
    }
  }
}
'''


# Declare a `list` with a type parameter
# # To declare types that have type parameters (internal types), like `list`, `dict`, `tuple`:
# # # # # For `< python v3.9`, import their equivalent version from the `typing` module
# # # # # Pass the internal type(s) as "type parameters" using square brackets: `[` and `]`

# in python v3.9, it would be:
# # # my_list: list[str]
# in ` < python v3.9`, it would be:
'''
from typing import List

my_list: List[str]
'''
# that's all standard python syntax for type declarations.
# Use that same standard syntax for model attributes with internal types
# So, in our example, we can make `tags` be specifically as "list of strings":

class TypeParameters(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []

@app.put('/type-parameters/{params_id}')
async def type_parameters(params_id: int, type_parameters: TypeParameters):
    results = {"params_id": params_id, "type_parameters": type_parameters}
    return results



# Set Types
### but then we think about it, and realize that tags shouldn't repeat,
### they would probably be unique strings.
### And Python has a special data type for sets of unique items, the `set`.
### Then we can declare `tags` as a set of strings

class SetTypes(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


@app.put('/set-types/{item_id}')
async def set_types(item_id: int, set_type: SetTypes):
    results = {"item_id": item_id, "set_type": set_type}
    return results

''''
request:
--------
endpoint: http://localhost:8000/set-types/234528
--------
{
    "name": "Set Types",
    "description": "details about set types",
    "price": 28437,
    "tax": 1.54273,
    "tags": [
        "hello",
        "hello",
        "world",
        "world"
    ]
}

another request fron swagger:
---------
{
  "name": "string",
  "description": "string",
  "price": 0,
  "tax": 0,
  "tags": [
      "mouse", 
      "monitor", 
      "keyboard", 
      "mouse", 
      "KEYBOARD", 
      "Monitor"
  ]
}
##############################################
##############################################
response:
----------
{
    "item_id": 234528,
    "set_type": {
        "name": "Set Types",
        "description": "details about set types",
        "price": 28437.0,
        "tax": 1.54273,
        "tags": [
            "hello",
            "world"
        ]
    }
}

another response:
------
{
  "item_id": 3456346,
  "set_type": {
    "name": "string",
    "description": "string",
    "price": 0,
    "tax": 0,
    "tags": [
      "keyboard",
      "KEYBOARD",
      "mouse",
      "Monitor",
      "monitor"
    ]
  }
}
'''

# With this, even if we receive a request with duplicate data, it will be converted to a set of unique items.
# And whenever we output that data, even if the source had duplicates, it will be output as a set of unique items.
# And it will be annotated/documented, accordingly too. (look at the OpenAPI Docs at : localhost:8000/docs at Schemas part)

##########################################################################
###
### Nested Models

# Each attribute of a Pydantic model has a type 
# But that type can itself be another Pydantic model.
# So, we can declare deeply nested JSON "objects" with specific attribute names, types and validations
# All that, artbitrarily nested.

'''
# Define a submodel
'''
class Book(BaseModel):
    id: int
    ISSN: str
    title: str
    author: str
    price: float
    tax: float | None = None
    category: str | None = None
    online_copy: str | None = None
  
class Library(BaseModel):
    name: str
    description: str | None = None
    is_verified: bool
    tags: set[str] = set()
    book: Book | None = None

@app.put('/nested-models/library/{l_id}')
async def nested_models(l_id: int, library: Library):
    profile = {"l_id": l_id, "library": library}
    return profile

# this would mean that FastAPI would expect a body similar to:
'''
request body::::
----------------
{
    "name": "Alice Library",
    "is_verified": true,
    "tags": [
        "science",
        "arts",
        "commerce"
    ],
    "book": {
        "id": 2324,
        "ISSN": "ISSN 0317-8471",
        "title": "The C Programming Language",
        "author": "Bjarne Stroustrup",
        "price": 10.37,
        "tax": 0.83,
        "category": "science",
        "online_copy": "https://www.amazon.com/Programming-Language-hardcover-4th/dp/0321958322"
    }
}
'''
# Again, doing just that declaration, with FastAPI we get:
#    - Editor Support (completion, etc.), even for nested models
#    - Data Conversion
#    - Data validation
#    - Automatic documentation


########################################

# Special types and validation
# # Apart from normal singular types like `str`, `int`, `float`, etc. we can use more comples singular types that inherit from `str`.
# # To see all the options you have, checkout:> Pydantic's Type Overview: https://docs.pydantic.dev/latest/concepts/types/
# For instance, as in the `Book` model we have a `online_copy` field, we can declare it to be an instance of Pydantic's `HttpUrl` instead of `str`

from pydantic import HttpUrl

class Books(BaseModel):
    name: str
    description: str | None = None
    author: str
    url: HttpUrl

class Lib(BaseModel):
    name: str
    description: str | None = None
    tags: set[str] = set()
    book: Books | None = None

@app.put('/special-types-and-validation/{book_id}')
async def special_types(book_id: int, lib: Lib):
    profile = {"book_id": book_id, "books": lib}
    return profile

# # The string will be checked to be a valid URL, and documented in JSON Schema / OpenAPI as such.



############################
# Attributes with lists of submodels
# # We can also use Pydantic models as subtypes of `list`, `set` etc.:

class ProductImage(BaseModel):
    name: str
    description: str
    url: HttpUrl

class Product(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    images: list[ProductImage] | None = None

@app.put('/attributes-list-submodels/{item_id}')
async def update_item(item_id: int, product: Product):
    response = {"item_id": item_id, "product": product}
    return response

################################
# Deeply Nested Models
# we can define arbitrarily deeply nested models

class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None

class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]

@app.post('/deeply-nested-models/offers/')
async def create_offer(offer: Offer):
    return offer

# Notice how `Offer` hasd a list of `Item`s, which in turn have an optional list of `Image`s


####################################
# Bodies of pure lists
# If the top level value of the JSON body we expect is a JSON array (a Python `list`), we can declare the type in the paramerter of the function, the sdame as in Pydantic models:

# ```images: List[Image]```
# or in Python 3.9 and above
# ```images: list[Image]```
# as in:

@app.post('/bodies-pure-lists/images/multiple')
async def create_multiple_images(images: list[Image]):
    return images


###################################
# Editor Support Everywhere
# # even for items inside of lists:
@app.post('/images/multiple/')
async def create_m_images(images: list[Image]):
    for image in images:
        print(f'image.url: {image.url}\nimage.name: {image.name}')
    return images

# You couldn't get this kind of editor suppoort if you were working directly with `dict` instead of Pydantic models.
# But you don't have to worry abotu them either, incoming dicts are converted automatically and your output is converted automatically to JSON too.

#################################
# Bodies of arbitrary `dict`S
# We can also declare a body as a `dict` with keys fo some type and values of some other type.

# This way, we don't have to know before thand what the valid field/attribute names are (as would be the case with Pydantic models).

# this would be useful if we want to receive keys that we don't already know.
# Another useful case is when we want to have keys of another type (e.g., int).
# that's what we are going to see here...
# in this case, we would accept any `dict` as long as it has `int` keys with `float` values.

@app.post('/index-weights/')
async def create_index_weights(weights: dict[int, float]):
    return weights


# Tip:::
'''
- Keep in mind that JSON only supports `str` as keys.
- But Pydantic has automatic data conversion.
- This means that, even though our API clients can only send string as keys, as long as those string contain pure integrs, Pydantic will convert tgem and validate them
- And the `dict` we receive as `weights` will acutally have `int` keys and `float` values.
'''

# Comment: with FastAPI we have the maximum flexibility provided by Pydantic Models, whle keeping our code simple, short and elegant.
# But with all the benefits:
# Editor support (completion everywhere)
# Data conversion (a.k.a. parsing/serialization)
# Data validation
# Scheme documentation
# Automatic docs