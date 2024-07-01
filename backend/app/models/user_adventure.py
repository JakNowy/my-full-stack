from sqlmodel import Field, Column, Integer, ARRAY, JSON, Relationship

from app.db.base_model import DatabaseModel, BaseIdModel


class UserAdventureBase(BaseIdModel):
    current_mission_step: int = 1
    completed_objectives: list[int] | None = Field(sa_column=Column(ARRAY(Integer)))
    is_complete: bool = False

    user_id: int = Field(foreign_key='user.id')
    adventure_id: int = Field(foreign_key='adventure.id')


class UserAdventure(DatabaseModel, UserAdventureBase, table=True):
    adventure_schema: dict = Field(sa_column=Column(JSON))

    user: "User" = Relationship(back_populates='user_adventures')
    adventure: "Adventure" = Relationship(back_populates='user_adventures')


from app.models.adventure import Adventure
from app.models.user import User
