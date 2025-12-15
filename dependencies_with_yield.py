# Dependencies with yield
# source: https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/

# FastAPI supports dependencies that do some "extra steps after finishing-> sometimes also called `exit code`, `cleanup code`, `teardown code`, `closing code`, `context manager exit code`"
# To do this, use `yield` instead of `return`, and write the extra steps (code) after

# # # # tip: make sure to use `yield` one single time per dependency

# # # # technical details:
# Any function that is valid to use with:
# - @contextlib.contextmanager [: source: https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager
# - @contextlib.asynccontextmanager [: source: https://docs.python.org/3/library/contextlib.html#contextlib.asynccontextmanager
# would be valid to use as a FastAPI dependency.
# In fact, FastAPI uses those two decorators internally.

# # A database dependency with `yield`
'''
For example, we could use this to create database session and close it after finishing.
Only the code prior to and including the `yield` statement is executed before creating a response:

```
async def get_deb():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()
```

The yielded value is what is injected into path operations and other dependencies:
The code following the `yield` statement is executed after the response:


# # tip:
- we can use `async` or regular functions
- FastAPI will do the right thing with each, the same as with normal dependencies
'''

# # A dependency with `yield` and `try`
'''
If we use a `try` block in a dependency with `yield`, we'll receive any exception that was thrown when using the dependency.

For example, if some code at some point in the middle, in another dependency or in a path operation, made a database transaction "rollback" or created any other exception, we would receive the exception in our dependency.

So, we can look for that specific exeception inside the dependency with `except SomeException`.

In the same way, we can use `finally` to make sure the exit steps are executed, no matter if there was an exception or not.

```
async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()
```
'''

# # Sub dependencies with `yield`
'''
We can have sub-dependencies and "trees" of sub-dependencies of any size and shape and any or all of them can use `yield`.

FastAPI will make sure that the "exit code" in each dependency with `yield` is rtun in the correct order.

For example, `dependency_c` can have a dependency on `dependency_b` and `dependency_a`:
'''
from typing import Annotated
from fastapi import FastAPI, Depends

async def generate_dep_a():
    return ""

async def generate_dep_b():
    return ""

async def generate_dep_c():
    return ""

class DepA:
    def __init__(self) -> None:
        pass

class DepB:
    def __init__(self) -> None:
        pass

async def dependency_a():
    dep_a = generate_dep_a()
    try:
        yield dep_a
    finally:
        dep_a.close()

async def dependency_b(dep_a: Annotated[DepA, Depends(dependency_a)]):
    dep_b = generate_dep_b()
    try:
        yield dep_b
    finally:
        dep_b.close()

async def dependency_c(dep_b: Annotated[DepB, Depends(dependency_b)]):
    dep_c = generate_dep_c()
    try:
        yield dep_c
    finally:
        dep_c.close()

# And all of them can use `yield`
# .....