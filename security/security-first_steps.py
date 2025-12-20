# Security - First Steps
# source: https://fastapi.tiangolo.com/tutorial/security/first-steps/

'''
Let's imagine that we have our backend API in some domain.
And we have frontend in another domain or in a different path of the same domain (or in a mobile application).
And we want to have a way for the frontend to authenticate with the backend, using a `username` and `password`
We can use "OAuth2" to build that with FastAPI
But let's save us the time of reading the full long specification just to find those little pieces of information we need.
let's use the tools provided by FastAPI to handle security.
'''

from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
import logfire

app = FastAPI()
logfire.configure()
logfire.instrument_fastapi(app)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get('/items/')
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {
        "token": token
    }



