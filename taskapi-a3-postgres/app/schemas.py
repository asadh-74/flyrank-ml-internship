from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(..., description="Task title (required, non-empty)")
    done: bool = False


class TaskUpdate(BaseModel):
    title: str = Field(..., description="Task title (required, non-empty)")
    done: bool = False


class TaskOut(BaseModel):
    id: int
    title: str
    done: bool
