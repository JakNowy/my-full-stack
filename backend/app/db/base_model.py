from datetime import datetime

from pydantic.alias_generators import to_camel
from sqlmodel import SQLModel, Field


class BaseModel(SQLModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True


class BaseIdModel(SQLModel):
    id: int


class TimestampFieldModel(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class DatabaseModel(TimestampFieldModel):
    id: int | None = Field(primary_key=True)

    def __str__(self):
        return f"id: {self.id}"


class ListOfIds(BaseModel):
    ids: list[int]
