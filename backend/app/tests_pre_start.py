import logging

from sqlalchemy import Engine
from sqlmodel import Session, select
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.db.session import engine
from app.common.deps import SessionDep

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init(session: SessionDep) -> None:
    try:
        session.exec(select(1))
    except Exception as e:
        logger.error(e)
        raise e


async def main() -> None:
    logger.info("Initializing service test prestard")
    await init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
