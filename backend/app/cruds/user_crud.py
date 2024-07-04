from datetime import timedelta

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Session
from fastcrud import FastCRUD

from app.common import security
from app.common.config import settings
from app.common.security import get_password_hash, verify_password
from app.common.utils import generate_new_account_email, send_email
from app.models.app import LoginResponse, Token
from app.models.user import UserCreate, User, UserBase, UserPublic


class UserCrud(FastCRUD[User, UserCreate, UserBase, UserBase, UserBase]):
    async def create(self, session: AsyncSession, user_create: UserCreate, commit: bool = True) -> LoginResponse:
        if await user_crud.count(session, email=user_create.email):
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists in the system.",
            )

        user = User.model_validate(
            user_create, update={"hashed_password": get_password_hash(user_create.password)}
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

        if settings.emails_enabled:
            email_data = generate_new_account_email(
                email_to=user_create.email, username=user_create.email,
                password=user_create.password
            )
            send_email(
                email_to=user_create.email,
                subject=email_data.subject,
                html_content=email_data.html_content,
            )
        user = UserPublic.model_validate(user)
        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return LoginResponse(
            token=Token(
                access_token=security.create_access_token(
                    user.id, expires_delta=access_token_expires
                )
            ),
            user=user
        )

    async def authenticate(self, session: Session, email: str, password: str) -> User | None:
        user = await self.get(session, return_as_model=True,
                                   schema_to_select=User, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user


user_crud = UserCrud(
    User,
)
