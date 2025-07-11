import logging

from sqlmodel import Session, create_engine, text

from app.core.config import get_settings

connect_args = {"check_same_thread": False}
engine = create_engine(get_settings().database_url, connect_args=connect_args)

logger = logging.getLogger(__name__)


def db_health_check():
    """Test if the database is reachable"""
    try:
        with Session(engine) as session:
            session.exec(text("SELECT 1"))
        logger.info(f"Connected to the database: {engine.name}")
        return True
    except Exception as e:
        logger.error(f"Failed connecting to the database: {e}")
        return False
