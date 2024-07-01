from sqlmodel import Relationship, Field

from app.db.base_model import DatabaseModel, BaseModel


class AdventureBase(BaseModel):
    title: str = Field(max_length=255)
    description: str = Field(max_length=255)


class Adventure(DatabaseModel, AdventureBase, table=True):
    missions: list["Mission"] = Relationship(back_populates='adventure')
    user_adventures: list["UserAdventure"] = Relationship(back_populates='adventure')


class MappedAdventure(AdventureBase):
    adventure_id: int
    user_adventure_id: int | None
    current_mission_step: int | None
    completed_objectives: list | None
    is_complete: bool | None
    user_id: int | None


from app.models.mission import Mission
from app.models.user_adventure import UserAdventure
