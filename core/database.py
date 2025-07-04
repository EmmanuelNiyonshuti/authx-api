from sqlmodel import create_engine, SQLModel, text
import logging
from sqlmodel import Session
from .config import get_settings

connect_args = {"check_same_thread": False}
engine = create_engine(
    get_settings().database_url,
    connect_args=connect_args
    )
# def init_db():
#     SQLModel.metadata.create_all(engine)

logger = logging.getLogger(__name__)

def db_health_check():
    """ Test if the database is reachable """
    try:
        with Session(engine) as session:
            session.exec(text("SELECT 1"))
        logger.info(f"Connected to the database: {engine.name}")
        return True
    except Exception as e:
        logger.error(f"Failed connecting to the database: {e}")
        return False
