import logging

from sqlalchemy import Engine
from sqlmodel import Session, select

from app.core.database import engine, init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def prestart_db(db_engine: Engine) -> None:
    try:
        with Session(db_engine) as session:
            # Try to create session to check if DB is awake
            session.exec(select(1))
    except Exception as e:
        logger.error(e)
        raise e


def init() -> None:
    # check db and seed db with initial data
    prestart_db(engine)
    with Session(engine) as session:
        init_db(session)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
