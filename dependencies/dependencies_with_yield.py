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
# In this case `dependency_c`, to execute its exit code, needs the value from `dependency_b`(here named `dep_b`) to still be available.
# And in turn `dependency_b` needs the value from `dependency_a`(here named `dep_`) to be available for its exit code.


# The same we, we could have some dependencies with `yield` and some other dependencies with `return`, and have some of those depend on the some of the others.
# And we could have a single dependency that requires several other dependencies with `yield`, etc
# We can have any combinations of dependencies that we want.
# FastAPI will make sure everything is run in the correct order.

# # Dependencies with `yield` and `HTTPException`
# We saw that we can use dependencies with `yield` and have `try` blocks that try to exetute some code and then run some exit code after `finally`.
# For example, we can raise a different exception, like `HTTPException`.

#TIP:::::
# This is a somewhat advanced technique, and in most the cases we won't really need it, as we can raise exceptions (including HTTPException) from inside of the rest of our application code, for example, in the path operation function.
# But it's where for us if we need it.

from fastapi import HTTPException, status
import logfire

app = FastAPI()
logfire.configure()
logfire.instrument_fastapi(app)

data = {
    "plumbus": {
        "description": "Freshly pickled plumbus",
        "owner": "Morty"
    },
    "portal-gun": {
        "description": "Gun to create portals",
        "owner": "Rick"
    }
}

class OwnerError(Exception):
    pass

def get_username():
    try:
        yield "Rick"
    except OwnerError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Owner error: {e}")
    

@app.get('/items/{item_id}')
async def get_item(item_id: str, username: Annotated[str, Depends(get_username)]):
    if item_id not in data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item not found!")
    item = data[item_id]
    if item["owner"] != username:
        raise OwnerError(username)
    return item

# If we want to catch exceptions and create a custom response based on that, create "Custom Exception Handler": https://fastapi.tiangolo.com/tutorial/handling-errors/#install-custom-exception-handlers

# # Dependencies with `yield` and `except`
# If we catch an exception using `except` in a dependency with `yield` and we don't raise it again (or raise a new exception), FastAPI won't be able to notice there was an exception, that same way that would happen with regular Python:

class InternalError(Exception):
    pass

def get_profile():
    try:
        yield "Doe"
    except InternalError:
        print("Oops, we didn't raise again, Britney 😱")

@app.get('/profiles/{profile_id}')
def get_profile_(profile_id: str, username: Annotated[str, Depends(get_profile)]):
    if profile_id == "portal-gun":
        raise InternalError(
            f"The portal gun is too dangerous to be owned by {username}"
        )
    if profile_id != "plumbus":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User profile not found, there's only a plumbus here"
        )
    return profile_id

# In this case, the client will see an "HTTP 500 Internal Server Error" response as it should, given that we are not raising an `HTTPException` or simialr, but the server will not have any logs or any other indication of what was the error 


# # Always `raise` in Dependencies with `yield` and `except`

def get_profile_v2():
    try:
        yield "Smith"
    except InternalError:
        print("We don't swallow the internal error here, we raise again 😎")
        raise

@app.get('/profiles-v2/{profile_id}')
def get_profile_v2_(profile_id: str, username: Annotated[str, Depends(get_profile_v2)]):
    if profile_id == "portal-gun":
        raise InternalError(
            f"The portal gun is too dangerous to be owned by {username}"
        )
    if profile_id != "plumbus":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User profile not found, there's only a plumbus here"
        )
    return profile_id

# Now the client will ge the same HTTP 500 Internal Server Error response, but the server will have our custom `InternlError` in the logs. 😎

# # Execution of dependencies with `yield`
# source: https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#execution-of-dependencies-with-yield

# info::
# Only one response will be sent to the client. It might be one of the error responses or it will be the response from the path operation.
# After one of those responses is sent, no other response can be sent.

# tip::
# If we raise any exception in the code from the path operation function, it wil be passed to the dependencies with yield, including `HTTPException`. In most cases we will want to re-raise that same exception or a new one from the dependency with `yield` to make sure it's properly handled.

# # Early exit and `scope`
#  Normally the exit code of dependencies with `yield` is executed after the response is sent to the client.
# But if we know that we won't need to use the dependency after returning from the path operation function, we can use `Depends(scope="function")` to tell FastAPI that it should close the dependency after the path operation function returns, but before the response is sent.

def get_test():
    try:
        yield "Rick"
    finally:
        print("Cleanup up before response is sent")

@app.get('/early-exit/test/')
def get_user_(username: Annotated[str, Depends(get_test, scope="function")]):
    return username

'''
`Depends()` receives a `scope` parameter that can be:
- "function": start the dependency before the path operation function that handles the request, end the dependency
                after the path operation functions ends, but before the response is sent back to the client. 
                So, the dependency function will be executed around the path operaiton function.

- "request": start the dependency before the path operation functin that handles the request (similar to when using "function"), but end after the response is sent back to the client. So, the dependency function will be executed around the request and response cycle.

If not specified and the dependency has `yield`, it will have a `scope` of "request" by default.

# # `scope` for sub-dependencies
When we declare a dependency with `scope="request"` (the default), any sub-dependency needs to also have a `scope` of `request`.

But a dependency with `scope` of "function" can have dependencies with `scope` of "function" and `scope` of "request".

This is because any dependency needs to be able to run its exit code before the sub-dependencies, as it might need to still use them during its exit code.
'''

# when "scope=request"
def get_test_with_request():
    try:
        yield "req"
    finally:
        print("Cleanup up after the response is sent")

@app.get('/early-exit/test-request/')
def get_user_me(username: Annotated[str, Depends(get_test_with_request, scope="request")]):
    return username

# # Dependencies with `yield`, `HTTPException`, `except` and Background Tasks
# Dependencies with `yield` have evolved over time to cover different use cases and fix some issues.

# If we want to see what has changed in differnet versions of FastAPI, we can read more about it in the advanced guide, in 
# "Advanced Dpeendencies - Dependencies with `yield` `HTTPException`, `except` and Background Tasks, ``: https://fastapi.tiangolo.com/advanced/advanced-dependencies/#dependencies-with-yield-httpexception-except-and-background-tasks"

# # Context Managers
# What are "Context Managers"
# "Context Managers" are any of those Python objects that we can use in a `with` statement.
# For example: we can use `with` to read a file: https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files
'''
with open("./somefile.txt") as f:
    contents = f.read()
    print(contents)
'''
# Underneath, the `open("./somefile.txt")` create an object that is called a "Content Manager".
# When the `with` block finishes, it makes sure to close the close, even if there were exceptions.
# When we create a dependency with `yield`, FastAPI will internally create a context manager for it, and combine it with some other related tools.

# Using context managers in dependencies with `yield`
# In Python, we can create Context Managers by create a class with two methods: __enter__() and __exit__(): https://docs.python.org/3/reference/datamodel.html#context-managers
# We can also use them inside of FastAPI dependencies with `yield` by using `with` or `async with` inside of the dependency function:
'''
class MySuperContextManager:
    def __init__(self):
        self.db = DBSession()

    def __enter__(self):
        return self.db
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()

async def get_db():
    with MySuperContextManager as db:
        yield db
'''

# TIP::::
# Another way to create a context manager is with:
# - @contextlib.contextmanager
# - @contextlib.asynccontextmanager
# using them to decorate a function with a single `yield`.
# That's what FastAPI users internally for dependencies with `yield`.
# But we don't have to use the decorators for FastAPI dependencies (and we shouldn't)
# FastAPI will do it for us internally.