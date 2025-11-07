from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import (
    database,
    metadata,
    engine
)
from .routes import (
    project,
    task
)

metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(title="Taller Code Challenge", lifespan=lifespan)

app.include_router(project.router)
app.include_router(task.router)
