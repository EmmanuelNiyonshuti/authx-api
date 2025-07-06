from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlmodel import Session, select

from passlib.context import CryptContext
import jwt

from ..models.user import User
from ..schemas.user import UserRead
from ..core.config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, password_hash) -> bool:
    return pwd_context.verify(plain_password, password_hash)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=get_settings().access_token_expire_minutes))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, get_settings().secret_key, algorithm=get_settings().algorithm)
    return encoded_jwt

def get_user_by_id(session: Session, user_id: str):
    user = session.exec(
        select(User).where(User.id == user_id)
        ).first()
    return UserRead.model_validate(user, from_attributes=True)
