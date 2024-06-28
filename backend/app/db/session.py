import os

from sqlmodel import select
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB_NAME = os.getenv("POSTGRES_DB")
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")

db_uri = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:5432/{POSTGRES_DB_NAME}"
)


engine = create_async_engine(db_uri)
session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
