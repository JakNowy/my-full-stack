from fastcrud import FastCRUD
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.mission import Mission, MissionObjectives
from app.models.objective import Objective


class MissionCrud(FastCRUD):
    @staticmethod
    async def get_missions_and_objectives(
        db: AsyncSession,
        adventure_id: int,
    ) -> list[MissionObjectives]:
        rows = await db.execute(
            select(Mission, Objective)
            .join(Objective, Mission.id == Objective.mission_id)
            .where(Mission.adventure_id == adventure_id)
        )
        objectives_by_mission_id = {}
        missions_by_mission_id = {}
        for mission, objective in rows:
            if mission.id not in objectives_by_mission_id:
                objectives_by_mission_id[mission.id] = []
            if mission.id not in missions_by_mission_id:
                missions_by_mission_id[mission.id] = mission.dict()

            objectives_by_mission_id[mission.id].append(objective)

        return [MissionObjectives(
            **missions_by_mission_id[mission_id], objectives=objectives
        ) for mission_id, objectives in objectives_by_mission_id.items()]


mission_crud = MissionCrud(
    Mission,
)
