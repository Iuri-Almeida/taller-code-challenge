import uuid
from datetime import (
    datetime,
    UTC
)
from fastapi import (
    APIRouter,
    HTTPException,
    Query
)

from src.database import database
from src.schemas.project import (
    ProjectCreate,
    ProjectOut,
    ProjectUpdate
)
from src.schemas.task import (
    TaskCreate,
    TaskOut
)
from src.models import (
    projects,
    tasks
)

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=ProjectOut, status_code=201)
async def create_project(project: ProjectCreate):
    project_id = str(uuid.uuid4())

    query = projects.insert().values(
        id=project_id, name=project.name, description=project.description, created_at=datetime.now(UTC)
    )

    await database.execute(query)

    return await database.fetch_one(projects.select().where(projects.c.id == project_id))


@router.get("/{project_id}", response_model=ProjectOut)
async def get_project(project_id: str):
    result = await database.fetch_one(projects.select().where(projects.c.id == project_id))

    if not result:
        raise HTTPException(404, "Project not found")

    return result


@router.put("/{project_id}", response_model=ProjectOut)
async def update_project(project_id: str, data: ProjectUpdate):
    existing = await database.fetch_one(projects.select().where(projects.c.id == project_id))

    if not existing:
        raise HTTPException(404, "Project not found")

    update_data = data.model_dump(exclude_unset=True)

    if update_data:
        await database.execute(projects.update().where(projects.c.id == project_id).values(**update_data))

    return await database.fetch_one(projects.select().where(projects.c.id == project_id))


@router.delete("/{project_id}", status_code=204)
async def delete_project(project_id: str):
    await database.execute(projects.delete().where(projects.c.id == project_id))


@router.post("/{project_id}/tasks/", response_model=TaskOut, status_code=201)
async def create_task(project_id: str, data: TaskCreate):
    project = await database.fetch_one(projects.select().where(projects.c.id == project_id))
    
    if not project:
        raise HTTPException(404, "Project not found")
    
    task_id = str(uuid.uuid4())
    
    query = tasks.insert().values(
        id=task_id,
        project_id=project_id,
        title=data.title,
        priority=data.priority,
        completed=data.completed,
        due_date=data.due_date
    )
    
    await database.execute(query)
    
    return await database.fetch_one(tasks.select().where(tasks.c.id == task_id))


@router.get("/{project_id}/tasks/", response_model=list[TaskOut])
async def list_tasks(project_id: str, limit: int = Query(20, ge=1, le=100), offset: int = 0):
    project = await database.fetch_one(projects.select().where(projects.c.id == project_id))

    if not project:
        raise HTTPException(404, "Project not found")

    query = (
        tasks.select()
        .where(tasks.c.project_id == project_id)
        .order_by(tasks.c.priority.desc())
        .limit(limit)
        .offset(offset)
    )

    return await database.fetch_all(query)
