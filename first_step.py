from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return { "message": "Hello World" }


class Desk:
    def __init__(self, desk_no: int, employer_name: str):
        self.desk_no = desk_no
        self.employer_name = employer_name
    
    def set(self, desk_no, employer_name):
        self.desk_no = desk_no
        self.employer_name = employer_name
    
    def get_desk_no(self):
        return self.desk_no, 

    def get_employer_name(self):
        return self.employer_name

@app.post("/{desk_no}/{employer_name}")
def route(desk_no: int, employer_name: str):
    myDesk = Desk(desk_no, employer_name)
    return { 
        "desk_no": {myDesk.get_desk_no()}, 
        "employer_name": {myDesk.get_employer_name()}
    }

## create a path operation
# path
    # URL: https://example.com/items/foo
    # /items/foo
# a "path" is also commonly called an "endpoint" or a "route"
# the "path" is the main way to separate "concerns" and "resources"

## operation (HTTP METHODS):
# POST
# GET
# PUT
# DELETE

## ...and the more exotic ones:
# OPTIONS
# HEAD
# PATCH
# TRACE
'''
In the HTTP protocol, we can communicate to each path using one or more of these "methods"

those HTTP methods to perform a specific action:
- POST: to create data
- GET: to read data
- PUT: to update data
- DELETE: to delete data

in OpenAPI, each of the HTTP methods is called an "operation"
'''

'''
from fastapi import FASTAPI

app = FastAPI()0
@app.get('/'): <- path operation decorator
async def root():
    return { "message": "Hello World" }


'''
