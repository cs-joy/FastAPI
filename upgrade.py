from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Student(BaseModel):
    id: str
    name: str
    session: str
    department: str

@app.get("/")
def read_root():
    return {"Hello": "World" }

@app.get("/students/{student_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return { "item_id": item_id, "q": q }

@app.put("/students/{student_id}")
def update_item(student_id: int, student: Student):
    return {"student_name": student.name, "student_id": student_id}

# https://fastapi.tiangolo.com/tutorial/#run-the-code

