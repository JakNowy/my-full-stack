from sqlmodel import Relationship, Field

from app.common.enums import ObjectiveType
from app.db.base_model import DatabaseModel, BaseModel


class ObjectiveBase(BaseModel):
    title: str = Field(max_length=255)
    description: str = Field(max_length=255)
    solution: str
    objective_type: ObjectiveType

    mission_id: int = Field(foreign_key="mission.id")


class Objective(DatabaseModel, ObjectiveBase, table=True):
    mission: "Mission" = Relationship(back_populates='objectives')


from app.models.mission import Mission
