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

# note:
# # it can be used by the frontend team (that can also be yourself)
# # it can be used by third party applications and systems.
# # and it can also be used by yourself, to debug, check and test the same application.

# # The `password` flow
'''
Now let's go back a bit and understand what is all that.
The `password` "flow" is one of the wats ("flows") defined in OAuth2, to handle security and authentication.
OAuth2 was designed so that the backend or API could be independent of the server that authenticate the user.
But in this cae, the same FastAPI application will handle the API and the authentication.
So, let's review it from that simplified point of view:
- The user types the `username` and `password` in the frontend and hits `Enter`
- The frontend (running in the user's browser) sends that `username` and `password` to a specific URL in our API (declared with tokenUrl="token")
- The API checks that `username` and `password`, and responds with a "token" 
....... continue : https://fastapi.tiangolo.com/tutorial/security/first-steps/#the-password-flow
'''

# FastAPI's `OAuth2PasswordBearer`
'''
FastAPI provides several tools, at different levels of abstraction, to implement these secucity features.
In this example, we are going to use OAuth2, with the Password flow, using Bearer token, We do that using the `OAuth2PasswordBearer` class.

When we create a n instance of the `OAuth2PasswordBearer` class we pass in the `tokenUrl` parameter. This parameter contains the URL that the client (the frontend running in the user's browser) will use the `username` and `password` in order to get a token.


'''


