# Get Current User
# source: https://fastapi.tiangolo.com/tutorial/security/get-current-user/

from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
import logfire
from pydantic import BaseModel

app = FastAPI()
logfire.configure()
logfire.instrument_fastapi(app)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = False

def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user

@app.get("/users/me")
async def read_users_me(current_user: Annotated[str, Depends(get_current_user)]):
    return current_user

# # Create a `get_current_user` dependency:
# `async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):`

# # Get the user:
'''
def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )

    
user = fake_decode_token(token)
return user
'''

# # Inject the current user:
# We can use the same `Depends` with our `get_current_yser` in the path operation:
# `async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):

# # Other models:
'''
We can now get the current user directly in the path operation functions and deal with the security mechanisms at the Dependency Injection level, using `Depends`:

And we can use any model or data for the security requirements (in this case, a Pydantic model `User`).

But we are not restricted to using some specific data model, class or type.

# Do we want to have a `str` or just a `dict` or a database class model instance directly? It all works the same way.

We actually don't have users that log in to your application but robots,  bots or other systems thatr have just an access token? Again it all works the same.

Just use  any kind of model, any kind of class, any kind of database that we need for our application. FastAPI has you covered with the dependency injection system.

'''

# # Code size:
'''
This example might seem verbose. Keep in mind that we are mixing 
    security,
    data models,
    utility functions and 
    path operations
in the same file. But here is the key point:
- The security and dependency injection stuff is written once.
- And we can make it as complex as we want. And still, have it written only once, in a single place. With all the flexibility.
- But we can have thousands of endpoints (path operations) using the same security system.
- And all of them (or any portion of them that we want) can take advantage of re-using these dependencies or any other dependencies we create.
- And all these thousands of path operations can be as small as 3 lines:

```
@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
```
'''

