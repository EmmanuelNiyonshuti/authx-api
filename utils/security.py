from fastapi import Depends, HTTPException
from passlib.context import CryptContext
import jwt
from sqlmodel import Session, select
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from ..models.user import User
from ..schemas.user import UserRead
from ..core.config import get_settings
from ..deps import SessionDep

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
def verify_password(plain_password, password_hash) -> bool:
    return pwd_context.verify(plain_password, password_hash)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=get_settings().access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, get_settings().secret_key, algorithm=get_settings().algorithm)

def get_user_by_id(session: Session, user_id: str):
    user = session.exec(
        select(User).where(User.id == user_id)
        ).first()
    return UserRead.model_validate(user, from_attributes=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(session: SessionDep, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, get_settings().secret_key, algorithms=[get_settings().algorithm])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = get_user_by_id(session, user_id)
    if user is None:
        raise credentials_exception
    return user