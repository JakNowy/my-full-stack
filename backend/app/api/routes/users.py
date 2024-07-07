from datetime import timedelta
from typing import Annotated

from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastcrud import EndpointCreator

from app.common import security
from app.common.deps import (
    UserDep,
    SessionDep,
    get_db,
)
from app.common.config import settings
from app.cruds.user_crud import user_crud
from app.models.app import Token, LoginResponse
from app.models.user import UserCreate, User, UserBase, UserPublic


class UserRouter(EndpointCreator):
    pass


user_router = UserRouter(
    session=get_db,
    model=User,
    crud=user_crud,
    create_schema=UserCreate,
    update_schema=UserBase,
)
user_router.add_routes_to_router(included_methods=['create'])
user_router = user_router.router


@user_router.post('/me')
async def endpoint(current_user: UserDep) -> UserPublic:
    return current_user


@user_router.post('/login')
async def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> LoginResponse:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    print(f"{form_data=}")
    user = await user_crud.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return LoginResponse(
        token=Token(
            access_token=security.create_access_token(
                user.id, expires_delta=access_token_expires
            )
        ),
        user=user
    )
