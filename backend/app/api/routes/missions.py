from fastcrud import EndpointCreator, JoinConfig
from sqlalchemy import join
from sqlalchemy.orm import joinedload
from sqlmodel import select

from app.common.deps import get_db, SessionDep
from app.cruds.adventure_crud import adventure_crud
from app.cruds.mission_crud import mission_crud, MissionCrud
from app.models.mission import Mission, MissionBase, MissionObjectives
from app.models.objective import Objective


class MissionRouter(EndpointCreator):
    def _read_items(self):
        """Creates an endpoint for reading multiple items from the database."""

        async def endpoint(
            db: SessionDep,
            adventure_id: int,
        ) -> list[MissionObjectives]:
            self.crud: MissionCrud
            return await self.crud.get_missions_and_objectives(db, adventure_id)

        return endpoint


mission_router = MissionRouter(
    session=get_db,
    model=Mission,
    path='/{adventure_id}',
    crud=mission_crud,
    create_schema=MissionBase,
    update_schema=MissionBase,
)
mission_router.add_routes_to_router(included_methods=['read_multi', ])
mission_router = mission_router.router
