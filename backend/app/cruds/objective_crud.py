from fastcrud import FastCRUD
from sqlmodel import select, and_
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.objective import Objective


class ObjectiveCrud(FastCRUD):
    @staticmethod
    async def verify_solution(
        db: AsyncSession,
        objective_id: int,
        solution: str
    ) -> int:

        result = await db.execute(select(
                Objective.mission_id
            )
            .where(
                and_(Objective.id == objective_id, Objective.solution == solution)
            )
        )
        if solved_objective_mission_id := result.scalar():
            return solved_objective_mission_id


objective_crud = ObjectiveCrud(
    Objective,
)
