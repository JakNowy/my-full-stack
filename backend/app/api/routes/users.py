from datetime import timedelta
from typing import Annotated

from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastcrud import EndpointCreator

from app.common import security
from app.common.deps import (
    CurrentUser,
    SessionDep,
    get_db,
)
from app.common.config import settings
from app.cruds.user_crud import user_crud
from app.models.app import Token
from app.models.user import UserCreate, User, UserBase


class UserRouter(EndpointCreator):
    def _read_item(self):
        async def endpoint(current_user: CurrentUser):
            return current_user

        return endpoint


user_router = UserRouter(
    session=get_db,
    model=User,
    crud=user_crud,
    create_schema=UserCreate,
    update_schema=UserBase,
)
user_router.add_routes_to_router(included_methods=['create', 'read'])
user_router = user_router.router


@user_router.post('/login')
async def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await user_crud.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )
