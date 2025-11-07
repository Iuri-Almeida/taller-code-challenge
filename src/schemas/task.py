from pydantic import BaseModel
from datetime import date


class TaskBase(BaseModel):
    title: str
    priority: int = 0
    completed: bool = False
    due_date: date | None = None

class TaskCreate(TaskBase): pass

class TaskUpdate(BaseModel):
    title: str | None = None
    priority: int | None = None
    completed: bool | None = None
    due_date: date | None = None

class TaskOut(TaskBase):
    id: str
    project_id: str

    class Config:
        orm_mode = True
