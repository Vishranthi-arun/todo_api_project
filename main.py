from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI()

class Todo(BaseModel):
    id: int
    task: str
    completed: bool
    created_at: datetime

todos_db = []

@app.post("/todos/", response_model=Todo)
def create_todo(todo: Todo):
    todo.id = len(todos_db) + 1
    todos_db.append(todo)
    return todo

@app.get("/todos/", response_model=List[Todo])
def read_todos():
    return todos_db

@app.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: int):
    for todo in todos_db:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: Todo):
    for i, existing_todo in enumerate(todos_db):
        if existing_todo.id == todo_id:
            todos_db[i] = Todo(id=existing_todo.id, **todo.dict())
            return todos_db[i]
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    for i, todo in enumerate(todos_db):
        if todo.id == todo_id:
            del todos_db[i]
            return None
    raise HTTPException(status_code=404, detail="Todo not found")