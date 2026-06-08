from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Todo(BaseModel):
    id: int
    task: str
    completed: bool

todos_db = []

@app.post("/todos/", response_model=Todo, status_code=status.HTTP_201_CREATED)
def create_todo(todo: Todo):
    todo.id = len(todos_db) + 1
    todos_db.append(todo)
    return todo

@app.get("/todos/", response_model=List[Todo], status_code=status.HTTP_200_OK)
def read_todos():
    return todos_db

@app.get("/todos/{todo_id}", response_model=Todo, status_code=status.HTTP_200_OK)
def read_todo(todo_id: int):
    todo = next((t for t in todos_db if t.id == todo_id), None)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=Todo, status_code=status.HTTP_200_OK)
def update_todo(todo_id: int, updated_todo: Todo):
    for idx, todo in enumerate(todos_db):
        if todo.id == todo_id:
            todos_db[idx] = updated_todo
            todos_db[idx].id = todo_id
            return todos_db[idx]
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int):
    global todos_db
    todos_db = [t for t in todos_db if t.id != todo_id]