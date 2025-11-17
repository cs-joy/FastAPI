from fastapi import FastAPI, HTTPException
import redis.asyncio as redisz
import os
import logfire

from uuid import uuid4
import json
from app.models import TodoItem
from typing import List


app = FastAPI()
logfire.configure()
logfire.instrument_fastapi(app)

redis_client = None

@app.on_event("startup")
async def startup_event():
    global redis_client
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    redis_client = redisz.from_url(redis_url, decode_responses=True)


@app.post('/todos/', response_model=TodoItem)
async def create_todo(todo: TodoItem):
    todo.id = str(uuid4())
    await redis_client.set(f"todo: {todo.id}", json.dumps(todo.dict()))
    
    return todo

@app.get('/todos/{todo_id}', response_model=TodoItem)
async def get_todo(todo_id: str):
    todo_data = await redis_client.get(f"todo: {todo_id}")
    if todo_data:
        return TodoItem.parse_raw(todo_data)
    raise HTTPException(status_code= 404, detail= "Todo not found!")

@app.get('/todos/', response_model= List[TodoItem])
async def get_all_todos():
    keys = await redis_client.keys("todo:*")
    todos = []
    for key in keys:
        todo_data = await redis_client.get(key)
        if todo_data:
            todos.append(TodoItem.parse_raw(todo_data))
    return todos

@app.put('/todos/{todo_id}', response_model=TodoItem)
async def update_todo(todo_id: str, updated_todo: TodoItem):
    existing_todo_data = await redis_client.get(f"todo: {todo_id}")
    if not existing_todo_data:
        raise HTTPException(status_code=404, detail= "todo not found!")
    existing_todo = TodoItem.parse_raw(existing_todo_data)
    update_data = updated_todo.dict(exclude_unset=True)
    updated_item = existing_todo.copy(update=update_data)
    await redis_client.set(f"todo:{todo_id}", json.dumps(updated_item.dict()))

    return updated_item


@app.delete('todos/{todo_id}', status_code=204)
async def delete_todo(todo_id: str):
    removed_count = await redis_client.delete(f"todo:{todo_id}")
    if removed_count == 0:
        raise HTTPException(status_code=404, detail="todo not found!")
    return





@app.on_event("shutdown")
async def shutdown_event():
    if redis_client:
        await redis_client.close()