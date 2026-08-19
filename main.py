from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(
    title="Task CRUD API",
    description="FlyRank Backend Week 2 Assignment A1 - To-Do CRUD API",
    version="1.0.0",
)

class TaskCreate(BaseModel):
    title: str
    done: bool = False

class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None

tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build CRUD API", "done": False},
    {"id": 3, "title": "Test with Swagger UI", "done": True},
]

@app.get("/")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(404, detail=f"Task {task_id} not found")

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    title = payload.title.strip()
    if not title:
        raise HTTPException(400, detail="Title is required and cannot be empty.")
    next_id = max((t["id"] for t in tasks), default=0) + 1
    task = {"id": next_id, "title": title, "done": False}
    tasks.append(task)
    return task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, payload: TaskUpdate):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        raise HTTPException(404, detail=f"Task {task_id} not found")
    if payload.title is None and payload.done is None:
        raise HTTPException(400, detail="Provide at least one field: title or done.")
    if payload.title is not None:
        title = payload.title.strip()
        if not title:
            raise HTTPException(400, detail="Title cannot be empty.")
        task["title"] = title
    if payload.done is not None:
        task["done"] = payload.done
    return task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return
    raise HTTPException(404, detail=f"Task {task_id} not found")

@app.get("/stats")
def stats():
    total = len(tasks)
    done = sum(t["done"] for t in tasks)
    return {"total": total, "done": done, "open": total - done}
