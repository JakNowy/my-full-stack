import logging
import asyncio
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.cruds.user_crud import user_crud
from app.db.session import SessionFactory
from app.common.config import settings
from app.models import User, UserCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init_db(session: AsyncSession) -> None:
    user = await session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    )
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = await user_crud.create_user(session=session, user_create=user_in)


async def main() -> None:
    logger.info("Creating initial data")
    async with SessionFactory() as db:
        await init_db(db)
    logger.info("Initial data created")


if __name__ == "__main__":
    asyncio.run(main())
