from fastapi import HTTPException

from sqlmodel import Session, select

from app.models.user import User, UserCreate, UserRead
from app.core.security import get_password_hash, verify_password


def register_user(session: Session, user_data: UserCreate) -> UserRead:
    user_exists = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="User already exists")
    pwd_hash = get_password_hash(user_data.password)
    new_user = User(**user_data.dict(exclude={"password"}), password=pwd_hash)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return UserRead.model_validate(new_user, from_attributes=True)

def authenticate_user(session: Session, form_data):
    user = session.exec(
        select(User).where(User.username == form_data.username)
    ).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
