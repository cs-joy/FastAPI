# Sub-dependencies
# source: https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/

# We can create dependencies that have sub-dependencies.
# They can be as deep as we need them to be.
# FasAPI will take care of solving them.

# # First dependency "dependable"
# We could create a first dependency "dependable" like:

from typing import Annotated
from fastapi import FastAPI, Depends, Cookie
import logfire

app = FastAPI()
logfire.configure()
logfire.instrument_fastapi(app)

def query_extractor(q: str | None = None):
    return q

def query_or_cookie_extractor(
        q: Annotated[str, Depends(query_extractor)],
        last_query: Annotated[str | None, Cookie()] = None,
):
    if not q:
        return last_query
    return q

@app.get('/sub-dependencies/items/')
async def view_query(query_or_default: Annotated[str, Depends(query_or_cookie_extractor)]):
    return {
        "q_or_cookie": query_or_default
    }

# It declares an optional query parameter `q` as a `str`, and then it just returns it.
# This is quite simple (not very useful), but will help us focus on how the sub-dependencies work.

# # Secondary dependency, "dependable" and "dependant"
# Then we can create another dependency function (a "dependable") that at the same time delcares a dependency of its own (so it is a "dependant") ``q: Annotated[str, Depends(query_extractor)],``

'''
Let's focus on the parameters declared:
- Even though this function is a dependency ("dependable") itself, it also declares another dependency (it "depends" on somethign else).
    - It depends on the `query_extractor`, and assigns the value returned by it to the parameter `q`
- It also declares an optional `last_query` cookie, as a `str`.
    - If the user didn't provide any query `q`, we use the last query used, which we saved to a cookie before.
'''

# # Use the dependency
'''
---------------------------------------|
            query_extractor            |
                ^^^^                   |
        query_or_cookie_extractor      |
                ^^^^^                  |
        /sub-dependencies/items/       |
                                       |
---------------------------------------|
'''

# # Using the same dependency multiple times
'''
If one of our dependencies is declared multiple times for the same path operation, for example
'''