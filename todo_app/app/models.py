from pydantic import BaseModel

class TodoItem(BaseModel):
    id: str | None = None
    title: str
    description: str | None = None
    completed: bool = False
