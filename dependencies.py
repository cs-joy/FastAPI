# Dependencies
# source: https://fastapi.tiangolo.com/tutorial/dependencies/

'''
FastAPI has a very powerful but intuitive "Dependency injection" system.
"Dependency injection": ->> also known as components, resources, providers, services, injectables 

# # What is "Dependency Injection"
"Dependency Injection" means, in programming, that there is a way for our code (in this case, our path operations) to declare things that it
requires to work and use: "dependencies".
And then, that system (in this case FastAPI) will take care of doing whatever is needed to provide our code with those needed dependencies ("inject" the dependencies).

This is very useful when we need to:
- Have shared logic (the same code logic again and again).
- Share database connections.
- Enforce security, authentication, role requirements, etc.
- And many other things....

All these, while minimizing code repetition.
'''

# # First Steps:::
# Let's see a very simple example. It will be so simple tha it is nmot very useful, for now.
# But this way we can focusd on how the "Dependency Injection" system works.

# # # Create dependency, or "dependable"
# let's first focus on the dependency.
# It is just a function that can take all the same parameters that a path operation function acan take:

from fastapi import FastAPI, Depends
import logfire
from typing import Annotated

app = FastAPI()
logfire.configure()
logfire.instrument_fastapi(app)

async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {
        "q": q,
        "skip": skip,
        "limit": limit
    }

@app.get('/items/')
async def get_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

@app.get('/users/')
async def get_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

'''
That's it.
2 lines
And it has the same shape and structure that all our path operation functions have.

We can think of it as a path operation function without the "decorator" (without the `@app.get('/some-path/')` ).

And it can return anything we want.

In this case, the dependency expects:
- An optional query parameter `q` that is a `str`.
- An optional query parameter `skip` that is an `int`, and by default is `0`.
- An optional query parameter `limit` that is an `int` and bu default is `100`.
'''

# note: The same way we use `Body`, `Query`, etc. with our path operation function parameters, use `Depends` with a new parameter.
# let's say....

from fastapi import Body, Query, HTTPException
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str
    description: str | None = None
    price: float = Field(..., gt=0)
    tax: float | None = 0.99

# dependency function
async def get_common_parameters(
        q: Annotated[str | None, Query(
            description="Search query",
            min_length=3,
            max_length=50,
            example="electronics"
        )] = None,

        skip: Annotated[int ,Query(
            ge=0,
            description="Number of products to skip",
            example=0
        )] = 0,

        limit: Annotated[int, Query(
            ge=1,
            le=100,
            description="Maximum number of items to return",
            example=10
        )] = 10,

        product: Annotated[Product | None, Body(
            description="The Product to create or update",
            example={
                "name": "GPU",
                "description": "Graphical Processing Unit",
                "price": 1249.234,
                "tax": 124.324
            }
        )] = None
):
    """
    Docstring for get_common_parameters
    
    :param q: Description
    :type q: Annotated[str | None, Query(description="Search query", min_length=3, max_length=50, example="electronics")]
    :param skip: Description
    :type skip: Annotated[int, Query(ge=0, description="Number of products to skip", example=0)]
    :param limit: Description
    :type limit: Annotated[int, Query(ge=1, le=100, description="Maximum number of items to retur", example=10)]
    :param product: Description
    :type product: Annotated[Product, Body(description="The Product to create or update", example={ "name": "GPU","description": "Graphical Processing Unit","price": 1249.234,"tax": 124.324 })]
    """
    return {
        "q": q,
        "skip": skip,
        "limit": limit,
        "product": product
    }

# example 1: using dependencies with query parameters only
@app.get('/query-params-only/product/')
async def read_product(commons: Annotated[dict, Depends(get_common_parameters)]):
    """
    Get items with pagination and filtering.
    
    - **q**: Search query
    :param commons: Description
    :type commons: Annotated[dict, Depends(get_common_parameters)]
    """
    return {
        "message": "Products retrieved",
        "params": commons,
        "products": [f"Item {i}" for i in range(commons["skip"], commons["skip"] + min(3, commons["limit"]))]
    }

# Although we use `Depends` in the parameters of our function the same way we use `Body`, `Query` etc., `Depends` works a bit differently.
# we only give `Depends` a single parameter
# this parameter must be something like a function.
# We don't call it directly (don't add the parenthesis at the end), we just pass it as a parameters to `Depends()`.
# And that function takes parameters in the same way that path operation functions do.

'''
Whenever a new request arrives, FastAPI will take care of:
- Calling our dependency ("dependable") functio with the correct parameters.
- Get the result from our function.
- Assign that result to the parameter in our path operation function.
# # # # # # # # # # # # # # # # # # # # #
                common_parameters
                       ^^^
                    - -   - -
                    |        |
                /items/      /users/

# # # # # # # # # # # # # # # # # # # # # # 
# This way we write shared code once and FastAPI takes care of calling it for our path operations.
'''

# # Share `Annotated` dependencies
# In the examples above (/items/ and /users/ section), we see that there's a tiny bit of code duplication.
# When we need to use the `common_parameters()` dependency, we have to write the whole parameter with the tpe annotation and `Depends()`:
'''
commons: Annotated[dict, Depends(common_parameters)]
'''
# But because we are using `Annotated`, we can store that `Annotated` value in a variable and use it in multiple places:

CommonsDep = Annotated[dict, Depends(common_parameters)]

@app.get('/commons-dep/items/')
async def view_items(commons: CommonsDep):
    return commons

@app.get('/commons-dep/users/')
async def read_users(commons: CommonsDep):
    return commons

# tip: this is just standard python, it's called a "type alias"
# This will be especially useful when we see it in a large code base where we use the same dependencies over and over again in many path operations.

# # To `async` or not `async`
# As dependencies will also be callewd : https://fastapi.tiangolo.com/tutorial/dependencies/#to-async-or-not-to-async

# # Integrated with OpenAPI: https://fastapi.tiangolo.com/tutorial/dependencies/#integrated-with-openapi

# # Simple usage
'''
If we look at it, path operation functions are declared to be used whenever a path and operation matches, and then
FastAPI takses care of calling the function with the correct parameters, extracting the data from the request.

Actually, all (or most) of the web frameworks work in this same way.

We never call those functions directly. They are called by our framework (in this case, FastAPI)

# With the dependency injection system, we can also tell FastAPI that our path operation function also "depends" on something else that should be executed before our path operatio function,
 and FastAPI will take care of executing it and "injecting" the results.

Other common terms for this same idea of "dependency injection" are:
- resources
- providers
- services
- injectables
- components
'''

# # FastAPI plug-ins
# source: https://fastapi.tiangolo.com/tutorial/dependencies/#fastapi-plug-ins

# # FastAPI compatibility
# The simplicity of the dependency injection system makes FastAPI compatible with:
# - all the relational database
# - NonSQL databases
# - external packages
# - external APIs
# - authentication and authorization systems
# - API usage monitoring systems
# - response data injection systems
# - etc

# # Simple and powerful
'''
source: https://fastapi.tiangolo.com/tutorial/dependencies/#simple-and-powerful

Although the hierachical dependency management system is very simple to define and use, it's still very powerful.

we can define dependencies that in turn can define dependencies themselves.

In the end, a hierachical tree of dependencies is built and the Depenedency Injection system takses care of solving all these 
dependencies for us (and their sub-dependencies) and providing (injecting) the results at each step.

For example, let's say we have 4 API endpoints (path operations):
 - /items/public/
 - /items/private
 - /users/{users_id}/activate
 - /items/pro/

Then we could add different permission requirements for each of them just with dependencies and sub-dependencies:

'''


