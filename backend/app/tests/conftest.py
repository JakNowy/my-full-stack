from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete
from sqlmodel.ext.asyncio.session import AsyncSession

from app.common.config import settings
from app.db.session import engine, init_db
from app.main import app
from app.models import Item, User
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_superuser_token_headers


@pytest.fixture(scope="session", autouse=True)
async def db() -> Generator[Session, None, None]:
    with AsyncSession(engine) as session:
        yield session
        await init_db(session)
        statement = delete(Item)
        await session.execute(statement)
        statement = delete(User)
        await session.execute(statement)
        await session.commit()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )
