from sqlmodel import Relationship, Field

from app.common.types.sql_types import BaseString
from app.db.base_model import DatabaseModel, BaseModel


class MissionBase(BaseModel):
    title: str = Field(max_length=255)
    description: str = Field(max_length=255)
    step: int
    adventure_id: int = Field(foreign_key="adventure.id")


class Mission(DatabaseModel, MissionBase, table=True):
    adventure: "Adventure" = Relationship(back_populates='missions')
    objectives: list["Objective"] = Relationship(back_populates='mission')


from app.models.adventure import Adventure
