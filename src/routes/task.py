from fastapi import (
    APIRouter,
    HTTPException
)

from src.database import database
from src.models import tasks
from src.schemas.task import (
    TaskOut,
    TaskUpdate
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.put("/{task_id}", response_model=TaskOut)
async def update_task(task_id: str, data: TaskUpdate):
    existing = await database.fetch_one(tasks.select().where(tasks.c.id == task_id))

    if not existing:
        raise HTTPException(404, "Task not found")

    update_data = data.model_dump(exclude_unset=True)

    if update_data:
        await database.execute(tasks.update().where(tasks.c.id == task_id).values(**update_data))

    return await database.fetch_one(tasks.select().where(tasks.c.id == task_id))


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: str):
    await database.execute(tasks.delete().where(tasks.c.id == task_id))
