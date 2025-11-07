import os

from databases import Database
from dotenv import load_dotenv
from sqlalchemy import (
    create_engine,
    MetaData
)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL.replace("+asyncpg", ""))
