import logging

from sqlmodel import Session, create_engine, text, select

from app.core.config import get_settings
from app.core.security import get_password_hash
from app.models.user import User

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


def init_db(session: Session) -> None:
    settings = get_settings()

    user = session.exec(
        select(User).where(User.email == settings.superuser_email)
    ).first()
    if user:
        if user.is_superuser:
            return {"message": "Database already initialized", "created": False}
        else:
            return {"message": f"user with {user.email} already exists"}
    superuser = User(
        username=settings.superuser_username,
        email=settings.superuser_email,
        password=get_password_hash(settings.superuser_password),
        is_superuser=True,
    )
    session.add(superuser)
    session.commit()
