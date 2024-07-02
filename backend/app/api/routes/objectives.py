from fastcrud import EndpointCreator

from app.common.deps import get_db, SessionDep
from app.cruds.objective_crud import objective_crud
from app.models.objective import Objective


class ObjectiveRouter(EndpointCreator):
    pass


mission_router = ObjectiveRouter(
    session=get_db,
    model=Objective,
    crud=objective_crud,
    create_schema=Objective,
    update_schema=Objective,
)
mission_router.add_routes_to_router(included_methods=['read', ])
mission_router = mission_router.router
