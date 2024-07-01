from sqlalchemy import union_all, func
from sqlalchemy.ext.asyncio import AsyncSession
from fastcrud import FastCRUD
from sqlmodel import select, not_, desc, and_

from app.models.adventure import Adventure, MappedAdventure
from app.models.user import User
from app.models.user_adventure import UserAdventure


class AdventureCrud(FastCRUD):
    async def read_mapped_adventures(
        self, session: AsyncSession, user_id: int, page: int, page_size: int
    ) -> list[MappedAdventure]:
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

        for row in rows:
            print(f"{row=}")
            m = MappedAdventure.model_validate(
                adventure_id=row[0],
                title=row[1],
                description=row[2],
                user_adventure_id=row[3],
                user_id=row[4],
                current_mission_step=row[5],
                completed_objectives=row[6],
                is_complete=row[7],
            )

        m = [MappedAdventure.model_validate(
            adventure_id=row[0],
            title=row[1],
            description=row[2],
            user_adventure_id=row[3],
            user_id=row[4],
            current_mission_step=row[5],
            completed_objectives=row[6],
            is_complete=row[7],
        ) for row in rows if True]
        print(f"{m=}")
        return m



adventure_crud = AdventureCrud(
    Adventure,
)
