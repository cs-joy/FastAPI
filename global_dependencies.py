# Global Dependencies
# # source: https://fastapi.tiangolo.com/tutorial/dependencies/global-dependencies/

'''
For some types of applications we might want to add dependencies to the whole application.

Similar to the way we can "add dependencies to the path operation decorators: https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/", we can add them to the FastAPI application.

In that case, they will be applied to all the path operations in the application:
'''

from fastapi import FastAPI, Depends, Header, HTTPException, status
from typing_extensions import Annotated
import logfire

async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="X-Token header invalid")
    
async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="X-Key header invalid")
    return x_key


app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])
logfire.configure()
logfire.instrument_fastapi(app)

@app.get('/global-dependencies/items/')
async def view_items():
    return [
        {"item": "Portal Gun"},
        {"item": "Plumbus"},
    ]

@app.get('/global-dependencies/users/')
async def view_users():
    return [
        {"username": "rick"},
        {"username": "morty"}
    ]


# And all the ideas in the section about "adding dependencies to the path operation decorators: https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/" still apply, but in this case, to all of the path operations in the app.

# # Dependencies for groups of path operations
# source: https://fastapi.tiangolo.com/tutorial/bigger-applications/