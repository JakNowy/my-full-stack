import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB_NAME = os.getenv("POSTGRES_DB")
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")

# db_uri = (
#     f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB_NAME}"
# )
db_uri = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:5432/{POSTGRES_DB_NAME}"
)
print(f"{db_uri=}")

# engine = create_engine(db_uri, pool_pre_ping=True)
# session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

engine = create_async_engine(db_uri)
session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
