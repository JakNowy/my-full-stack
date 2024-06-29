from typing import Any

from sqlmodel import Session, select
from fastcrud import FastCRUD

from app.common.security import get_password_hash, verify_password
from app.models import UserCreate, User, UserUpdate


class UserCrud(FastCRUD):
    async def create_user(self, *, session: Session, user_create: UserCreate) -> User:
        db_obj = User.model_validate(
            user_create, update={"hashed_password": get_password_hash(user_create.password)}
        )
        await session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


    def update_user(self, *, session: Session, db_user: User, user_in: UserUpdate) -> Any:
        user_data = user_in.model_dump(exclude_unset=True)
        extra_data = {}
        if "password" in user_data:
            password = user_data["password"]
            hashed_password = get_password_hash(password)
            extra_data["hashed_password"] = hashed_password
        db_user.sqlmodel_update(user_data, update=extra_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


    async def get_user_by_email(self, session: Session, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        session_user = result.one_or_none()
        return session_user


    async def authenticate(self, session: Session, email: str, password: str) -> User | None:
        db_user = await self.get_user_by_email(session=session, email=email)
        if not db_user:
            return None
        if not verify_password(password, db_user.hashed_password):
            return None
        return db_user


user_crud = UserCrud(
    User,
)
