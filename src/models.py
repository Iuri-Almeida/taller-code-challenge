import uuid
from sqlalchemy import (
    Table,
    Column,
    String,
    Integer,
    Boolean,
    Date,
    DateTime,
    ForeignKey
)
from datetime import (
    datetime,
    UTC
)
from .database import metadata

projects = Table(
    "projects",
    metadata,
    Column("id", String, primary_key=True, default=str(uuid.uuid4())),
    Column("name", String, nullable=False),
    Column("description", String),
    Column("created_at", DateTime, default=datetime.now(UTC)),
)

tasks = Table(
    "tasks",
    metadata,
    Column("id", String, primary_key=True, default=lambda: str(uuid.uuid4())),
    Column("project_id", String, ForeignKey("projects.id", ondelete="CASCADE")),
    Column("title", String, nullable=False),
    Column("priority", Integer, default=0),
    Column("completed", Boolean, default=False),
    Column("due_date", Date)
)
