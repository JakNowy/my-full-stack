from sqlmodel import Field, Column, Integer, ARRAY, JSON, Relationship

from app.db.base_model import DatabaseModel, BaseModel


class UserAdventureIn(BaseModel):
    adventure_id: int = Field(foreign_key='adventure.id')


class UserAdventureBase(UserAdventureIn):
    is_complete: bool = False
    current_mission_step: int = 1
    completed_objectives: list[int] | None = Field(sa_column=Column(ARRAY(Integer)), default=[])

    user_id: int = Field(foreign_key='user.id')


class UserAdventureOut(UserAdventureBase):
    adventure_schema: dict = Field(sa_column=Column(JSON))
    id: int


class UserAdventure(DatabaseModel, UserAdventureOut, table=True):
    user: "User" = Relationship(back_populates='user_adventures')
    adventure: "Adventure" = Relationship(back_populates='user_adventures')


from app.models.adventure import Adventure
from app.models.user import User
