from fastapi import APIRouter

from app.api.routes import login, users, utils, user_adventures, missions

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.user_router, prefix="/users", tags=["users"])
api_router.include_router(user_adventures.user_adventure_router, prefix="/user_adventures", tags=["user_adventures"])
api_router.include_router(missions.mission_router, prefix="/missions", tags=["missions"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
