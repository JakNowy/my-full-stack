import logging
import asyncio
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import session
from app import crud
from app.common.config import settings
from app.models import User, UserCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init_db(session: AsyncSession) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # from app.common.engine import engine
    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    user = await session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    )
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = await crud.create_user(session=session, user_create=user_in)


async def main() -> None:
    logger.info("Creating initial data")
    async with session() as db:
        await init_db(db)
    logger.info("Initial data created")


if __name__ == "__main__":
    asyncio.run(main())
