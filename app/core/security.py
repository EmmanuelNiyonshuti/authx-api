from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from sqlmodel import Session, select

from passlib.context import CryptContext
import jwt
import uuid

from app.models.user import User, UserRead
from app.core.config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)


def create_access_token(user_id: uuid.UUID, expires_delta: timedelta | None = None) -> str:
    # to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=get_settings().access_token_expire_minutes)
    )
    to_encode = {"user_id": str(user_id), "exp": expire}
    # to_encode.update({"user_id": user_id, "exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, get_settings().secret_key, algorithm=get_settings().algorithm
    )
    return encoded_jwt

def get_user_by_id(session: Session, user_id: str):
    user = session.exec(select(User).where(User.id == uuid.UUID(user_id))).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {user_id} does not exist",
        )
    return UserRead.model_validate(jsonable_encoder(user), from_attributes=True)
