from pydantic import (
    BaseModel,
    Field
)
from datetime import datetime


class ProjectBase(BaseModel):
    name: str = Field(min_length=20)
    description: str | None = None

class ProjectCreate(ProjectBase): pass

class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

class ProjectOut(ProjectBase):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True
