from sqlmodel import Relationship, Field

from app.common.types.sql_types import BaseString
from app.db.base_model import DatabaseModel, BaseModel


class AdventureBase(BaseModel):
    title: str = Field(max_length=255)
    description: str = Field(max_length=255)


class Adventure(DatabaseModel, AdventureBase, table=True):
    missions: list["Mission"] = Relationship(back_populates='adventure')


from app.models.mission import Mission
