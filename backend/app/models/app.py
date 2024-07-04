from sqlmodel import Field, SQLModel

from app.models.user import UserPublic


class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: int | None = None


class LoginResponse(SQLModel):
    token: Token
    user: UserPublic


class NewPassword(SQLModel):
    new_password: str = Field(min_length=8, max_length=40)
