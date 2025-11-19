# Header Parameters

# we can define Header parameters the same way we define `Query`, `Path` and `Cookie` parameters.


from typing import Annotated
import logfire
from fastapi import FastAPI, Header

app = FastAPI()
logfire.configure()
logfire.instrument_fastapi(app)


@app.get('/items/')
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}


# Declare `Header` parameters
# https://fastapi.tiangolo.com/tutorial/header-params/#declare-header-parameters


# Automatic conversion
# source: https://fastapi.tiangolo.com/tutorial/header-params/#automatic-conversion
# ...

# Before setting `convert_underscores` to `False`, bear in mind that some HTTP proxies and servers disallow the usage of headers with underscores.

@app.get('/view-items/')
async def view_items(
    strange_header: Annotated[str | None, Header(convert_underscores=True)] = None,
):
    return {"strange_header": strange_header}

# Duplicate headers
# ------------------
# it is possible to receive duplicate headers. That means, the same header with multiple values
# We can define those cases using a list in the type declaration.
# we will receive all the values from the duplicate header as a Python `list`.
# For instance, to declare a header of `X-Token` that can appear more than once, we can write:
@app.get('/duplicate-headers/items/')
async def dup_headers(x_token: Annotated[list[str] | None, Header()] = None):
    return {"X-Token values": x_token}