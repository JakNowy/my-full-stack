from fastapi import Query
from fastcrud import EndpointCreator

from app.common.deps import get_db, CurrentUser, SessionDep
from app.cruds.adventure_crud import adventure_crud
from app.models.adventure import Adventure, AdventureBase, MappedAdventure, \
    AdventureOut


class AdventureRouter(EndpointCreator):
    def _read_items(self):
        async def endpoint(
            current_user: CurrentUser,
            db: SessionDep,
            page: int = Query(1, alias="page"),
            items_per_page: int = Query(10, alias="itemsPerPage"),
        ) -> list[MappedAdventure | AdventureOut]:
            return await self.crud.read_mapped_adventures(
                session=db,
                page=page,
                page_size=items_per_page,
                user_id=current_user.id,
            )

        return endpoint


adventure_router = AdventureRouter(
    session=get_db,
    model=Adventure,
    crud=adventure_crud,
    create_schema=AdventureBase,
    update_schema=AdventureBase,
)
adventure_router.add_routes_to_router(included_methods=['read_multi', ])
adventure_router = adventure_router.router
