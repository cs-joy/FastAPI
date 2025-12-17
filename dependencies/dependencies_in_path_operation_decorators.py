# Dependencies in path operation decorators
# source: https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/

'''
In some cases we don't really need the return value of a dependency inside our path operation function.
Or the dependency doesn't return a value.
But we still need it to be executed/solved.
For those cases, instead of declaring a path operation function parameter with `Depends`, we can add a `list` of `dependencies` to the path operation decorator.
'''

# # Add `dependencies` to the path operation decorator
# # # The path operation decorator receives an optional argument `dependencies`.
# # # It should a `list` of `Depends()`:

from typing import Annotated
from fastapi import FastAPI, Depends, Header, HTTPException, status
import logfire

app = FastAPI()
logfire.configure()
logfire.instrument_fastapi(app)

async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="X-Token header invalid")

async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="X-Key header invalid")
    return x_key

@app.get('/dependencies_in_path_operation_decorators/items/', dependencies=[Depends(verify_token), Depends(verify_key)])
async def view_items():
    return [
        {"item": "Foo"},
        {"item": "Bar"}
    ]
# These dependencies will be executed/solved the same way as normal dependencies. But their value (if they return any) won't be passed to our path operation funciton.

# ::::: info :::::
# In this example we use invented custom headers `X-Key` and `X-Token`.
# But in real cases, when implementing security, we would get more benefits from usinbg the integrated "Security utilites: https://fastapi.tiangolo.com/tutorial/security/"

# # Dependencies erors and returns values
# We can use the same dependency functions we use normally.

# # # Dependency requirements
# They can declare request requirements (like header) or other sub-dependencies:

# # Raise exceptions
# These dependencies can `raise` exceptions, the same as normal dependencies

# # Return values
# And they can return values or not, the values won't be used.
# So, we can reuse a normal dependency (that returns a value) we already ise somewhere else and even though the value won't be used, the dependency will be executed.

# # Dependencies for a group of path operations
# Later, when reading about how to structure bigger applications (Bigger applications - Multiple fiels: https://fastapi.tiangolo.com/tutorial/bigger-applications/), possibly with multiple files,
# we will learn how to single `dependencies` parameter for a group of path operations.

# # Global dependencies
# Next we will see how to add dependencies to the whole `FastAPI` application, so that they apply to each path operation.