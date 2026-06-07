from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI()

class Todo(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool = False
    created_at: datetime

todos = []

@app.post("/todos/", response_model=Todo)
def create_todo(todo: Todo):
    todo_dict = todo.dict()
    todo_dict["id"] = len(todos) + 1
    todos.append(todo_dict)
    return todo_dict

@app.get("/todos/", response_model=List[Todo])
def get_todos():
    return todos

@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: Todo):
    for i, t in enumerate(todos):
        if t["id"] == todo_id:
            todos[i] = todo.dict()
            return todos[i]
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}", response_model=Todo)
def delete_todo(todo_id: int):
    for i, t in enumerate(todos):
        if t["id"] == todo_id:
            del todos[i]
            return {"id": todo_id}
    raise HTTPException(status_code=404, detail="Todo not found")