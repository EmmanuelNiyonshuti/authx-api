from collections.abc import Generator
from typing import Annotated

import jwt

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlmodel import Session

from .core.database import engine
from .core.config import get_settings
from .core.security import get_user_by_id
from .models.user import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login/access_token"
    )

def get_db() -> Generator[Session, None, None]:
    """ generator-based dependency to yield a fresh DB session"""
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]

async def get_current_user(session: SessionDep, token: TokenDep):
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

CurrentUser = Annotated[User, Depends(get_current_user)]
