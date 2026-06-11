from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI()

class Todo(BaseModel):
    id: Optional[int] = None
    task: str
    completed: bool = False
    created_at: Optional[datetime] = None

todos_db: List[Todo] = []

@app.get("/todos", response_model=List[Todo])
def get_todos():
    return todos_db

@app.post("/todos", response_model=Todo)
def create_todo(todo: Todo):
    if not todos_db:
        todo.id = 1
    else:
        todo.id = todos_db[-1].id + 1
    todo.created_at = datetime.now()
    todos_db.append(todo)
    return todo

@app.get("/todos/{todo_id}", response_model=Todo, responses={404: {"detail": "Todo not found"}})
def get_todo(todo_id: int):
    for todo in todos_db:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.put("/todos/{todo_id}", response_model=Todo, responses={404: {"detail": "Todo not found"}})
def update_todo(todo_id: int, todo_update: Todo):
    for i, todo in enumerate(todos_db):
        if todo.id == todo_id:
            todos_db[i].task = todo_update.task
            todos_db[i].completed = todo_update.completed
            return todos_db[i]
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}", responses={404: {"detail": "Todo not found"}})
def delete_todo(todo_id: int):
    global todos_db
    todos_db = [todo for todo in todos_db if todo.id != todo_id]
    return {"message": "Todo deleted"}