from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class TodoIn(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoOut(TodoIn):
    id: int

todos = []

@app.post("/todos/", response_model=TodoOut)
def create_todo(todo: TodoIn):
    new_todo = {"id": len(todos) + 1, **todo.dict()}
    todos.append(new_todo)
    return new_todo

@app.get("/todos/", response_model=List[TodoOut])
def get_todos():
    return todos

@app.get("/todos/{todo_id}", response_model=TodoOut)
def get_todo(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.put("/todos/{todo_id}", response_model=TodoOut)
def update_todo(todo_id: int, todo: TodoIn):
    for i, t in enumerate(todos):
        if t["id"] == todo_id:
            updated_todo = {"id": t["id"], **todo.dict()}
            todos[i] = updated_todo
            return updated_todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}", response_model=TodoOut)
def delete_todo(todo_id: int):
    for i, t in enumerate(todos):
        if t["id"] == todo_id:
            deleted_todo = todos.pop(i)
            return deleted_todo
    raise HTTPException(status_code=404, detail="Todo not found")