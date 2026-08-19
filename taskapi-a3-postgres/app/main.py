from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from .db import pool
from .repository import TaskRepository
from .schemas import TaskCreate, TaskOut, TaskUpdate

repo = TaskRepository(pool)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the table if missing, seed three example tasks only on first run.
    repo.init_table()
    repo.seed_if_empty()
    yield


app = FastAPI(title="Task API", lifespan=lifespan)


# Uniform error body: {"error": "..."} instead of FastAPI's default
# {"detail": "..."} — matches the spec every stage of this assignment used.
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


@app.get("/health")
def health():
    try:
        repo.ping()
        return {"status": "ok", "db": "ok"}
    except Exception:
        return JSONResponse(
            status_code=503, content={"status": "error", "db": "down"}
        )


@app.get("/tasks", response_model=list[TaskOut])
def list_tasks():
    return repo.get_all()


@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int):
    task = repo.get_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(payload: TaskCreate):
    if not payload.title or not payload.title.strip():
        raise HTTPException(status_code=400, detail="Title is required")
    return repo.create(payload.title, payload.done)


@app.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, payload: TaskUpdate):
    if not payload.title or not payload.title.strip():
        raise HTTPException(status_code=400, detail="Title is required")
    task = repo.update(task_id, payload.title, payload.done)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    deleted = repo.delete(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return None
