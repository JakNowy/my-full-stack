from fastapi import Query, HTTPException
from fastcrud import EndpointCreator
from starlette import status

from app.common.deps import get_db, UserDep, SessionDep
from app.cruds.adventure_crud import adventure_crud
from app.cruds.objective_crud import objective_crud
from app.cruds.user_adventure_crud import user_adventure_crud
from app.cruds.user_crud import user_crud
from app.models.adventure import MappedAdventure, AdventureOut, Adventure
from app.models.objective import ObjectiveSolution
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
            if await user_adventure_crud.get(
                db, adventure_id=user_adventure_in.adventure_id,
                user_id=current_user.id
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='You already have bought this adventure'
                )

            adventure: Adventure = await adventure_crud.get(
                db, id=user_adventure_in.adventure_id,
                schema_to_select=AdventureOut, return_as_model=True
            )
            if adventure.price > current_user.money:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Adventure costs {adventure.price}, '
                           f'but you only have {current_user.money}'
                )
            current_user.money -= adventure.price
            user_crud.update(db, current_user, allow_multiple=True)

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


@user_adventure_router.post('/solve_objective')
async def solve_objective(
    db: SessionDep,
    current_user: UserDep,
    solution_in: ObjectiveSolution,
) -> UserAdventureOut:
    if not (
            objective_mission_id := await objective_crud.verify_solution(
                db, solution_in.objective_id, solution_in.solution
            )
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid solution'
        )
    if not (
        user_adventure := await user_adventure_crud.verify_user_adventure(
            db, solution_in.user_adventure_id, solution_in.objective_id,
            objective_mission_id, current_user.id
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid user_adventure'
        )

    if not await user_adventure_crud.verify_mission_step(
        db, user_adventure, objective_mission_id
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid mission step'
        )

    return await user_adventure_crud.advance_user_adventure(
        db, user_adventure, solution_in.objective_id, objective_mission_id
    )
