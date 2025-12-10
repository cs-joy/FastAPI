# Classes as Dependencies
# source: https://fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/

# Before diving deeper into the "Dependency Injection System", let's upgrade the previous example.

# # A `dict` from the previous example
# In the previous example, we were returning a  `dict` from our dependency ("dependable"):

from typing import Annotated
from fastapi import FastAPI, Depends
import logfire

app = FastAPI()
logfire.configure()
logfire.instrument_fastapi(app)


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {
        "q": q,
        "skip": skip,
        "limit": limit
    }

@app.get('/profiles/')
async def read_profiles(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

@app.get('/users/')
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

# But then we get a `dict` in the parameter `commons` of the path operation function.
# And we know that editors can't provide a lot of support (like completion) for `dict`s, becaise thye can't know their keys and value types.

# We can do better...
'''
# # What makes a dependency
Up to now we have seen dependencies declared as functions.

But that's not the only way to declare dependencies (although it would probably be the more common)

The key factor is that a dependency should be "callable"

# A "callable" in python is anything that python can "call" like a function.

So, if we have an object `something` (that might not be a function) and we can "call" it (execute it) like:
```
something()
```
or
```
something(some_argument1, some_argument2, some_keyword_argument="foo")
```
then it is a "callable"
'''

# # Classes as dependencies
# We might be notice that to create an instance of Python class, we use that same syntax.

'''
For example::
'''
class Cat:
    def __init__(self, name: str):
        self.name = name

hex = Cat(name="Mr Hex")

# in this case `hex` is an instance of the class `Cat`.

# And to create `hex`, we are "calling" `Cat`.

# So, a python class is also "callable"

# Then in FastAPI, we could user a Python class as a dependency

# What FastAPI actually checks is that it is a "callable" (function, class or anything class) and the parameters defined.

# If we pass a "callable" as a dependency in FastAPI, it will analyze the parameters for that "callable", and process them in the same as the parameters for a path operation function. including sub-dependencies.

# That also applies to callable with no parameters. The same as it would be for path operation functions with no parameters.

# Then, we can change the dependecny "dependable" `common_parameters` from above to the class `CommonQueryParams`:

fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"},
]

class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int  = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get('/items/')
async def view_items(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response


# # Type annotation vs `Depends`
# source: https://fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/#type-annotation-vs-depends

# we could actually write just:
# commons: Annotated[Any, Depends(CommonQueryParams)]

# # Shortcut
'''
But we see that we are having some code repetition here, writing `CommonQueryParams` twice:
`commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]`

FastAPI provides a shortcut for these cases, in where the dependency is specifically a class that FastAPI will "call" to create an instance of the class itself.
For those specific cases, we can do the following:
instead of writing:
`commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]`
... we write
`commons: Annotated[CommonQueryParams, Depends()]`

We declare the dependency as the type of the parameter, and we use `Depends()` without any parameter, instead of having to write the full class again inside of `Depends(CommonQueryParams)`.

so, the above example (path function) would then look like:
```
async def view_items(commons: Annotated[CommonQueryParams, Depends()]):
...... so on
```

... and FastAPI will know what to do.

'''