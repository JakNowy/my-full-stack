from fastapi import Query
from fastcrud import EndpointCreator

from app.common.deps import get_db, UserDep, SessionDep
from app.cruds.user_adventure_crud import user_adventure_crud
from app.models.adventure import MappedAdventure, AdventureOut
from app.models.user_adventure import UserAdventure, UserAdventureIn, \
    UserAdventureBase, UserAdventureOut


class UserAdventureRouter(EndpointCreator):
    def _read_items(self):
        async def endpoint(
            current_user: UserDep,
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

    def _create_item(self):
        async def endpoint(
            db: SessionDep,
            current_user: UserDep,
            user_adventure_in: UserAdventureIn,
        ) -> UserAdventureOut:
            return await self.crud.create(
                db=db,
                user_adventure_base=UserAdventureBase.model_validate(
                    user_adventure_in, update={'user_id': current_user.id}
                )
            )

        return endpoint


user_adventure_router = UserAdventureRouter(
    session=get_db,
    model=UserAdventure,
    crud=user_adventure_crud,
    create_schema=UserAdventureIn,
    update_schema=UserAdventureIn,
)
user_adventure_router.add_routes_to_router(included_methods=['read_multi', 'create'])
user_adventure_router = user_adventure_router.router
