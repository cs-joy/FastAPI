# Response Status Code
# source: https://fastapi.tiangolo.com/tutorial/response-status-code/

# The same way we can specify a response model, we can also declare the HTTp status code used for the response with the parameter `status_code` in any of the path operations:
'''
- @app.get()
- @app.post()
- @app.put()
- @app.put()
- @app.delete()
'''

from fastapi import FastAPI
import logfire
from pydantic import BaseModel

app = FastAPI()
logfire.configure()
logfire.instrument_fastapi(app)


@app.get('/items/', status_code=201)
async def create_item(name: str):
    return {"name": name}

# note: `status_code` can alternatively also receive an `IntEnum`, such as Python's http.HTTPStatus: https://docs.python.org/3/library/http.html#http.HTTPStatus

# Some response codes indicate that the response does not have a body.

# About HTTP status codes
'''
numeric status code of 3 digits

* 100-199 are for "information". we can use them directly, responses with these status codes cannot have a body.
* 200-299 are for "Successfull" responses. 
    # `200` is the default status code which means everything was "OK"
    # `201` "Created, it is commonly used after creating a new record in the database
    # `204` "No Content". this response is used when there is no content to return to the client, and so the response must not have a body
* 300-399 are for "Redirection". Responses with these status codes may or may not have a body, except for `304`, "Not Modified", which must not have one.
* 400-499 are for "Client error" responses. These are the second type we would probably use the most.
    # `404` for a "Not Found" response
    # `400` for generic errors from the client
* 500-599 are for server errors. we almost never use them directly, when something goes wrong at some part in our applciation codee, or server, it will automatically return one of these status codes.


summary:
1. Informational responses (100-199)
2. Successful responses (200-299)
3. Redirection messages (300-399)
4. Client error responses (400-499)
5. Server error responses (500-599)

read more about status code: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
'''

# Shortcut to remember the names
from fastapi import status

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item_2(name: str):
    return {"name": name}

# for changing the default -> https://fastapi.tiangolo.com/advanced/response-change-status-code/

