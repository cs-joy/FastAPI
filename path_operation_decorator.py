'''
path operation decorators:
1. @app.get()
2. @app.post()
3. @app.put()
4. @app.delete()

and the more exotic ones:
1. @app.options()
2. @app.head()
3. @app.trace()
'''

from fastapi import FastAPI, HTTPException, status, Request
from pydantic import BaseModel, ValidationError
from typing import Optional

from fastapi.responses import JSONResponse

app = FastAPI(title="Path Operation Decorators Demo")

# sample data model
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: float

# in-memory storage
items_db = {
    1: Item(name="Laptop", description="Gaming Laptop", price=1200.05, tax=0.1),
    2: Item(name="Mouse", description="Wireless mouse", price=25.50, tax=0.08)
}

## @app.get() - retrieve data ##
@app.get("/")
async def root():
    return {
        "status": "running",
        "message": "FastAPI Path Operation Demo"
    }

@app.get("/items/")
async def get_items():
    return items_db

@app.get("/items/{item_id}")
async def get_item_v1(item_id: int): # without exception handling
    return items_db[item_id] # will return "ERROR -> Exception in ASGI application" when item_id isn't exist

@app.get("/v2/items/{item_id}")
async def get_item_v2(item_id: int): # with proper exception handling
    if  item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

## @app.post() - create new data ##
@app.post('/items/')
async def create_item(item: Item): # without error handling
    print(f'max(items_db.keys()): {max(items_db.keys())}')
    new_id = max(items_db.keys()) + 1
    items_db[new_id] = item
    return {
        "id": new_id,
        "item": item
    }

# with erro handling
@app.post('/v2/items')
async def create_item_v2(item: Item):
    try:
        new_id = max(items_db.keys())+1
        items_db[new_id] = item
        return {
            "id": new_id,
            "item": item
        }
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors()
        )

# error handling
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code= 422,
        content={
            "details": [
                {
                    "type": error["type"],
                    "loc": error["loc"],
                    "msg": error["msg"],
                    "input": error.get("inputs")
                }
                for error in exc.errors()
            ]
        }
    )


# @app.put() - Update existing data
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = item
    return {
        "message": f"{item_id} no. Item updated",
        "item": item
    }

# @app.delete() - Delete data
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail= "Item not found")
    removed_item = items_db.pop(item_id)
    return {
        "message": f"Item {item_id} removed",
        "deleted_item": removed_item
    }

# @app.options() - get communication options
@app.options('/items/')
async def options_items():
    return {
        "allowed_method": ["GET", "POST", "OPTIONS", "HEAD"],
        "content-type": "application/json"
    }

@app.options("/items/{item_id}")
async def options_item(item_id: int):
    return {
        "allowed_method": ["GET", "PUT", "DELETE", "OPTIONS", "HEAD"],
        "content_type": "application/json"
    }


# @app.head() - get headers only (same as GET but without body)
@app.head('/items/')
async def head_items():
    return {
        "message": "Headers only"
    }

@app.head('/items/{item_id}')
async def head_item(item_id: int):
    return "Item headers"

@app.head('/v2/items/{item_id}')
async def head_item_v2(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail= "Item not found")
    return {
        "message": "Item headers"
    }


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: Optional[float] = None

@app.patch('/items/{item_id}')
async def partial_update_item(item_id: int, item_update: ItemUpdate):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail= "Item not found")
    current_item = items_db[item_id]

    # update only the fields that are provided
    update_data = item_update.dict(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=404, detail="Item not found")
    
    for field, value in update_data.items():
        setattr(current_item, field, value)
    
    items_db[item_id] = current_item

    return {
        "messgae": "Item partially updated",
        "updated_fields": list(update_data.keys()),
        "item": current_item
    }