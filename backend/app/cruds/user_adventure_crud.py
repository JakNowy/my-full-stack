from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from fastcrud import FastCRUD
from sqlmodel import select, and_

from app.cruds.mission_crud import mission_crud
from app.models.adventure import Adventure, MappedAdventure, AdventureOut
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
                user_adventure_id=row[3],
                user_id=row[4],
                current_mission_step=row[5],
                completed_objectives=row[6],
                is_complete=row[7],
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
            mission.id: [objective.id for objective in mission.objectives] for
            mission in adventure_missions
        }


user_adventure_crud = UserAdventureCrud(
    UserAdventure,
)
