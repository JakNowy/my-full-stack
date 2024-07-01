from pydantic import EmailStr
from sqlmodel import Field

from app.db.base_model import DatabaseModel, BaseModel


class UserBase(BaseModel):
    email: EmailStr = Field(unique=True, max_length=255)
    first_name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class User(DatabaseModel, UserBase, table=True):
    is_superuser: bool = False
    hashed_password: str


class UserPublic(UserBase):
    id: int


class UsersPublic(BaseModel):
    data: list[UserPublic]
    count: int
