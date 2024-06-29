from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Session
from fastcrud import FastCRUD

from app.common.security import get_password_hash, verify_password
from app.models import UserCreate, User, UserUpdate


class UserCrud(FastCRUD[User, UserCreate, UserUpdate, UserUpdate, UserUpdate]):
    async def create(self, session: AsyncSession, user_create: UserCreate, commit: bool = True) -> User:
        db_obj = User.model_validate(
            user_create, update={"hashed_password": get_password_hash(user_create.password)}
        )
        session.add(db_obj)
        if commit:
            await session.commit()
        return db_obj

    async def authenticate(self, session: Session, email: str, password: str) -> User | None:
        user = await user_crud.get(session, return_as_model=True,
                                   schema_to_select=User, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user


user_crud = UserCrud(
    User,
)
