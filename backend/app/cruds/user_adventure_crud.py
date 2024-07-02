from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from fastcrud import FastCRUD
from sqlmodel import select, and_

from app.common.deps import UserDep
from app.cruds.mission_crud import mission_crud
from app.cruds.objective_crud import objective_crud
from app.models.adventure import Adventure, MappedAdventure, AdventureOut
from app.models.mission import Mission
from app.models.user_adventure import UserAdventure, UserAdventureBase, \
    UserAdventureOut


class UserAdventureCrud(FastCRUD):
    async def create(
        self, db: AsyncSession,
        user_adventure_base: UserAdventureBase, commit: bool = True
    ) -> UserAdventureOut:

        adventure_schema = await self.generate_adventure_schema(
            db=db, adventure_id=user_adventure_base.adventure_id
        )
        user_adventure = UserAdventure.model_validate(
            user_adventure_base,
            update={'adventure_schema': adventure_schema}
        )

        db.add(user_adventure)
        await db.commit()
        await db.refresh(user_adventure)
        return user_adventure

    @staticmethod
    async def read_mapped_adventures(
        session: AsyncSession, user_id: int, page: int, page_size: int
    ) -> list[MappedAdventure | AdventureOut]:
        query = (
            select(
                Adventure.id,
                Adventure.title,
                Adventure.description,
                Adventure.price,
                UserAdventure.id,
                UserAdventure.user_id,
                UserAdventure.current_mission_step,
                UserAdventure.completed_objectives,
                UserAdventure.is_complete,
            )
            .outerjoin(UserAdventure, and_(Adventure.id == UserAdventure.adventure_id,
                                      UserAdventure.user_id == user_id))
            .order_by(func.coalesce(UserAdventure.id, -1).desc(), Adventure.id)
        )
        rows = await session.execute(query)

        return [
            MappedAdventure(
                id=row[0],
                title=row[1],
                description=row[2],
                price=row[3],
                user_adventure_id=row[4],
                user_id=row[5],
                current_mission_step=row[6],
                completed_objectives=row[7],
                is_complete=row[8],
            ) if row[3] else
            Adventure(
                id=row[0],
                title=row[1],
                description=row[2],
            ) for row in rows
        ]

    @staticmethod
    async def generate_adventure_schema(db: AsyncSession, adventure_id: int):
        adventure_missions = await mission_crud.get_missions_and_objectives(
            db, adventure_id=adventure_id
        )

        return {
            mission.id: [objective.id for objective in mission.objectives]
            for mission in adventure_missions
        }

    @staticmethod
    async def verify_user_adventure(
        db: AsyncSession, user_adventure_id: int, objective_id: int,
        mission_id: str, user_id: int
    ):
        if (
            user_adventure := await user_adventure_crud.get(
                db, id=user_adventure_id, user_id=user_id, return_as_model=True,
                schema_to_select=UserAdventure
            )
        ) and (
            objective_id in user_adventure.adventure_schema.get(
                str(mission_id), []
            )
        ):
            return user_adventure

    async def verify_mission_step(
        self, db: AsyncSession, user_adventure: UserAdventure, mission_id: int
    ) -> bool:
        mission: Mission = await mission_crud.get(db, id=mission_id)
        return user_adventure.current_mission_step == mission['step']

    @staticmethod
    async def advance_user_adventure(
        db: AsyncSession, user_adventure: UserAdventure,
        objective_id: int, mission_id: int
    ):

        if objective_id not in user_adventure.completed_objectives:
            user_adventure.completed_objectives.append(objective_id)

        if set(user_adventure.adventure_schema[str(mission_id)]) == set(
                user_adventure.completed_objectives):
            if str(mission_id + 1) in user_adventure.adventure_schema:
                user_adventure.current_mission_step += 1
                user_adventure.completed_objectives = []
            else:
                user_adventure.is_complete = True

        await user_adventure_crud.update(
            db, user_adventure, allow_multiple=True, id=user_adventure.id
        )
        return user_adventure


user_adventure_crud = UserAdventureCrud(
    UserAdventure,
)
